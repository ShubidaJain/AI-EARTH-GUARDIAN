//
//  WifiNetworkSharingProvider.swift
//  App Transport Security Settings
//
//  Created by CU_Student26 on 17/08/26.
//

import AccessorySetupKit.ASAccessory
import AccessoryTransportExtension
import Foundation
import Network
import os.log
import WiFiInfrastructure

fileprivate let logger = Logger(subsystem: subsystem, category: "WiFiNetworkSharingProvider")

/// Responsible for managing WiFi network sharing operations and events.
///
/// `WiFiNetworkSharingProvider` fetches Wi-Fi networks
/// via `WINetworkSharingProvider`, which requires an `ASAccessory` parameter.
@available(iOS 26.2, *)
final class WiFiNetworkSharingProvider {

	/// The accessory associated with this extension session.
	private let accessory: ASAccessory

	/// Task for managing network event listening.
	private var networkEventTask: Task<Void, Never>?

	// MARK: -

	/// Initializer.
	init(for accessory: ASAccessory) {
		self.accessory = accessory
	}

	/// Activates the sharing provider.
	///
	/// This method should be called after initialization, and
	/// when accessory is ready to receive network events.
	func activate() {
		guard networkEventTask == nil else { return }
		logger.info("Activate \(self.accessory.bluetoothIdentifier?.uuidString ?? "")")
		networkEventTask = Task {
			await listenForNetworkEvents()
		}
	}

	/// Invalidates the sharing provider and releases all associated resources.
	///
	/// This method cleans up all references and should be
	/// called when the session is no longer needed.
	func invalidate() {
		guard networkEventTask != nil else { return }
		networkEventTask?.cancel()
		networkEventTask = nil

		logger.info("Invalidated")
	}

	// MARK: -

	/// Monitors Wi-Fi network events and handles user consent flow for network sharing.
	///
	/// This method establishes an asynchronous stream to monitor
	/// network sharing events from the WiFiInfrastructure framework.
	///
	/// It handles two primary scenarios:
	/// - **New shareable network available**: Automatically presents sharing UI when a new
	///   shareable network becomes available
	/// - **App-requested sharing**: Responds to explicit sharing requests from the accessory
	private func listenForNetworkEvents() async {
		do {
			let sharingProvider = try await WINetworkSharingProvider(for: accessory)
			for try await event in sharingProvider.networkEvents() {
				guard !Task.isCancelled else { break }
				await handleNetworkEvent(event, using: sharingProvider)
			}
		} catch {
			logger.error("### Failed to get network events: \(error)")
		}
	}

	/// Handles individual network events.
	///
	/// Helper function to serialize and send networks to the accessory.
	private func handleNetworkEvent(_ event: WINetworkSharingProvider.NetworkEvent, using sharingProvider: WINetworkSharingProvider) async {
		if event.appRequestedSharing || event.newShareableNetworkAvailable {
			do {
				let _ = try await sharingProvider.presentAskToShareUI(scanProvider: nil)
				// Handle scan response if needed

			} catch {
				logger.error("### Failed to present Ask To Share UI: \(error)")
			}
		}

		// Encoding example
		do {
			let _ = try JSONEncoder().encode(event.networks)
			// TODO: Send data to accessory

		} catch {
			logger.error("### Failed to encode networks: \(error)")
		}
	}
}

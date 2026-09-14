import Foundation
import CoreLocation
import Combine

@MainActor
final class LocationManager: NSObject, ObservableObject {

    private let manager = CLLocationManager()

    @Published var location: CLLocation?
    @Published var authorizationStatus: CLAuthorizationStatus

    override init() {

        authorizationStatus = manager.authorizationStatus

        super.init()

        manager.delegate = self
        manager.desiredAccuracy = kCLLocationAccuracyBest
        manager.distanceFilter = kCLDistanceFilterNone
    }

    func requestPermission() {

        manager.requestWhenInUseAuthorization()
    }

    func startUpdatingLocation() {

        print("📍 Starting location updates")

        manager.startUpdatingLocation()
    }

    func stopUpdatingLocation() {

        manager.stopUpdatingLocation()
    }
}

extension LocationManager: CLLocationManagerDelegate {

    func locationManager(
        _ manager: CLLocationManager,
        didChangeAuthorization status: CLAuthorizationStatus
    ) {

        print(
            "📍 Authorization changed:",
            status.rawValue
        )

        authorizationStatus = status

        switch status {

        case .authorizedWhenInUse,
             .authorizedAlways:

            print("✅ Location permission granted")

            manager.startUpdatingLocation()

        case .denied:

            print("❌ Location permission denied")

        case .restricted:

            print("❌ Location restricted")

        case .notDetermined:

            print("⏳ Location permission not determined")

        @unknown default:

            break
        }
    }

    func locationManager(
        _ manager: CLLocationManager,
        didUpdateLocations locations: [CLLocation]
    ) {

        guard let latestLocation = locations.last else {
            return
        }

        print(
            "📍 Location received:",
            latestLocation.coordinate.latitude,
            latestLocation.coordinate.longitude
        )

        location = latestLocation
    }

    func locationManager(
        _ manager: CLLocationManager,
        didFailWithError error: Error
    ) {

        let nsError = error as NSError

        print(
            "❌ Location error:",
            nsError.domain,
            nsError.code,
            nsError.localizedDescription
        )

        // kCLErrorLocationUnknown = temporary.
        // Don't treat it as a permanent failure.
        if nsError.code == 0 {
            print("⏳ Waiting for a location fix...")
        }
    }
}

import SwiftUI
import CoreLocation

struct ContentView: View {

    @StateObject private var viewModel = RiskViewModel()
    @StateObject private var locationManager = LocationManager()
    @State private var selectedTab = "Home"

    private let backgroundColor = Color(hex: "071B16")
    private let cardColor = Color(hex: "102A22")
    private let accentColor = Color(hex: "75D69A")

    var body: some View {
        NavigationStack {
            ZStack {
                backgroundColor
                    .ignoresSafeArea()

                Group {
                    switch selectedTab {
                    case "Map":
                        mapTabContent
                    case "Insights":
                        insightsTabContent
                    case "Settings":
                        settingsTabContent
                    default:
                        dashboardContent
                    }
                }
                .frame(maxWidth: .infinity, maxHeight: .infinity)
            }
            .safeAreaInset(edge: .bottom, spacing: 0) {
                bottomNavigation
            }
            .toolbar(.hidden, for: .navigationBar)
        }
        .preferredColorScheme(.dark)
    }

    // MARK: - Home Dashboard

    private var dashboardContent: some View {
        ScrollView(showsIndicators: false) {
            VStack(alignment: .leading, spacing: 24) {
                headerSection
                locationSection

                if let prediction = viewModel.prediction {
                    RiskCardView(prediction: prediction)
                } else {
                    emptyRiskSection
                }

                if let location = locationManager.location {
                    VStack(alignment: .leading, spacing: 12) {
                        sectionHeader(
                            title: "Wildfire Monitoring",
                            subtitle: "Live regional risk map"
                        )

                        MapView(
                            location: location,
                            gridPredictions: viewModel.gridPredictions,
                            gridRadius: viewModel.gridRadius,
                            gridPoints: viewModel.gridPoints
                        )
                        .frame(height: 300)
                        .clipShape(RoundedRectangle(cornerRadius: 22))
                        .overlay {
                            RoundedRectangle(cornerRadius: 22)
                                .stroke(.white.opacity(0.08), lineWidth: 1)
                        }

                        if !viewModel.gridPredictions.isEmpty {
                            GridRiskSummaryView(
                                predictions: viewModel.gridPredictions
                            )
                        }
                    }
                } else {
                    locationPermissionCard
                }

                loadingAndErrorSection
                analyzeButton
                footerSection
            }
            .padding(.horizontal, 20)
            .padding(.top, 18)
            .padding(.bottom, 24)
        }
    }

    // MARK: - Header

    private var headerSection: some View {
        HStack(spacing: 12) {
            ZStack {
                RoundedRectangle(cornerRadius: 16)
                    .fill(accentColor.opacity(0.14))
                    .frame(width: 52, height: 52)

                Image(systemName: "leaf.fill")
                    .font(.system(size: 24, weight: .semibold))
                    .foregroundStyle(accentColor)
            }

            VStack(alignment: .leading, spacing: 4) {
                Text("EARTH GUARDIAN")
                    .font(.system(size: 18, weight: .bold, design: .rounded))
                    .tracking(1.1)
                    .foregroundStyle(.white)

                Text("AI-powered wildfire protection")
                    .font(.caption)
                    .foregroundStyle(.white.opacity(0.55))
            }

            Spacer()

            Image(systemName: "globe.asia.australia.fill")
                .font(.system(size: 23))
                .foregroundStyle(accentColor)
        }
    }

    // MARK: - Location

    private var locationSection: some View {
        VStack(alignment: .leading, spacing: 8) {
            Text("YOUR LOCATION")
                .font(.caption2.weight(.bold))
                .tracking(1.4)
                .foregroundStyle(accentColor)

            if let location = locationManager.location {
                HStack(spacing: 8) {
                    Image(systemName: "location.fill")
                        .foregroundStyle(accentColor)

                    Text(
                        "\(location.coordinate.latitude, specifier: "%.4f"), \(location.coordinate.longitude, specifier: "%.4f")"
                    )
                    .font(.subheadline.monospaced())
                    .foregroundStyle(.white.opacity(0.85))
                }
            } else {
                Text("Location access required")
                    .font(.subheadline)
                    .foregroundStyle(.white.opacity(0.6))
            }
        }
    }

    // MARK: - Empty Risk State

    private var emptyRiskSection: some View {
        VStack(alignment: .leading, spacing: 12) {
            Label(
                "CURRENT ASSESSMENT",
                systemImage: "waveform.path.ecg"
            )
            .font(.caption2.weight(.bold))
            .tracking(1.1)
            .foregroundStyle(accentColor)

            Text("No analysis yet")
                .font(.title2.bold())
                .foregroundStyle(.white)

            Text("Analyze your current location to generate an AI-powered wildfire risk assessment.")
                .font(.subheadline)
                .foregroundStyle(.white.opacity(0.6))
                .fixedSize(horizontal: false, vertical: true)
        }
        .padding(20)
        .frame(maxWidth: .infinity, alignment: .leading)
        .background(cardColor)
        .clipShape(RoundedRectangle(cornerRadius: 22))
        .overlay {
            RoundedRectangle(cornerRadius: 22)
                .stroke(.white.opacity(0.08), lineWidth: 1)
        }
    }

    // MARK: - Location Permission

    private var locationPermissionCard: some View {
        VStack(spacing: 12) {
            Image(systemName: "location.circle.fill")
                .font(.system(size: 36))
                .foregroundStyle(accentColor)

            Text("Enable Location")
                .font(.headline)
                .foregroundStyle(.white)

            Text("Your location helps calculate nearby wildfire risk and display regional predictions.")
                .font(.subheadline)
                .multilineTextAlignment(.center)
                .foregroundStyle(.white.opacity(0.6))

            Button {
                locationManager.requestPermission()
            } label: {
                Text("Allow Location Access")
                    .font(.subheadline.bold())
                    .foregroundStyle(backgroundColor)
                    .padding(.horizontal, 20)
                    .padding(.vertical, 12)
                    .background(accentColor)
                    .clipShape(Capsule())
            }
        }
        .frame(maxWidth: .infinity)
        .padding(24)
        .background(cardColor)
        .clipShape(RoundedRectangle(cornerRadius: 22))
    }

    // MARK: - Loading and Errors

    private var loadingAndErrorSection: some View {
        VStack(spacing: 12) {
            if viewModel.isLoading {
                ProgressView("Analyzing fire risk...")
                    .tint(accentColor)
                    .foregroundStyle(.white.opacity(0.75))
            }

            if viewModel.isLoadingGrid {
                ProgressView("Generating regional risk map...")
                    .tint(accentColor)
                    .foregroundStyle(.white.opacity(0.75))
            }

            if let error = viewModel.errorMessage {
                Label(error, systemImage: "exclamationmark.triangle.fill")
                    .font(.caption)
                    .foregroundStyle(.red)
                    .padding(14)
                    .frame(maxWidth: .infinity, alignment: .leading)
                    .background(.red.opacity(0.10))
                    .clipShape(RoundedRectangle(cornerRadius: 14))
            }
        }
    }

    // MARK: - Analyze Button

    private var analyzeButton: some View {
        Button {
            analyzeCurrentLocation()
        } label: {
            HStack(spacing: 10) {
                Image(systemName: "sparkles")
                Text("Analyze Current Location")
                    .fontWeight(.bold)
            }
            .foregroundStyle(backgroundColor)
            .frame(maxWidth: .infinity)
            .padding(.vertical, 17)
            .background(accentColor)
            .clipShape(RoundedRectangle(cornerRadius: 16))
        }
        .disabled(viewModel.isLoading || viewModel.isLoadingGrid)
        .opacity(viewModel.isLoading || viewModel.isLoadingGrid ? 0.6 : 1)
    }

    private func analyzeCurrentLocation() {
        guard let location = locationManager.location else {
            locationManager.requestPermission()
            return
        }

        let latitude = location.coordinate.latitude
        let longitude = location.coordinate.longitude

        viewModel.fetchRisk(
            latitude: latitude,
            longitude: longitude
        )

        viewModel.fetchGrid(
            latitude: latitude,
            longitude: longitude
        )
    }

    // MARK: - Map Tab

    private var mapTabContent: some View {
        VStack(alignment: .leading, spacing: 14) {
            VStack(alignment: .leading, spacing: 5) {
                Text("Wildfire Map")
                    .font(.title2.bold())
                    .foregroundStyle(.white)

                Text("Explore regional fire-risk predictions")
                    .font(.subheadline)
                    .foregroundStyle(.white.opacity(0.55))
            }
            .padding(.horizontal, 20)
            .padding(.top, 18)

            if let location = locationManager.location {
                MapView(
                    location: location,
                    gridPredictions: viewModel.gridPredictions,
                    gridRadius: viewModel.gridRadius,
                    gridPoints: viewModel.gridPoints
                )
                .clipShape(RoundedRectangle(cornerRadius: 20))
                .padding(.horizontal, 12)
                .frame(maxWidth: .infinity, maxHeight: .infinity)
            } else {
                Spacer()
                locationPermissionCard
                    .padding(.horizontal, 20)
                Spacer()
            }

            if viewModel.isLoadingGrid {
                ProgressView("Generating risk map...")
                    .tint(accentColor)
                    .foregroundStyle(.white)
                    .frame(maxWidth: .infinity)
                    .padding(.bottom, 12)
            }
        }
        .frame(maxWidth: .infinity, maxHeight: .infinity)
    }

    // MARK: - Insights Tab

    private var insightsTabContent: some View {
        ScrollView(showsIndicators: false) {
            VStack(alignment: .leading, spacing: 22) {
                VStack(alignment: .leading, spacing: 5) {
                    Text("Risk Insights")
                        .font(.title2.bold())
                        .foregroundStyle(.white)

                    Text("Regional wildfire intelligence")
                        .font(.subheadline)
                        .foregroundStyle(.white.opacity(0.55))
                }

                if !viewModel.gridPredictions.isEmpty {
                    GridRiskSummaryView(
                        predictions: viewModel.gridPredictions
                    )
                } else {
                    VStack(spacing: 12) {
                        Image(systemName: "chart.bar.xaxis")
                            .font(.system(size: 35))
                            .foregroundStyle(accentColor)

                        Text("No regional insights yet")
                            .font(.headline)
                            .foregroundStyle(.white)

                        Text("Analyze your current location to generate regional wildfire-risk statistics.")
                            .font(.subheadline)
                            .foregroundStyle(.white.opacity(0.55))
                            .multilineTextAlignment(.center)

                        Button {
                            analyzeCurrentLocation()
                        } label: {
                            Text("Analyze Location")
                                .font(.subheadline.bold())
                                .foregroundStyle(backgroundColor)
                                .padding(.horizontal, 20)
                                .padding(.vertical, 12)
                                .background(accentColor)
                                .clipShape(Capsule())
                        }
                    }
                    .frame(maxWidth: .infinity)
                    .padding(25)
                    .background(cardColor)
                    .clipShape(RoundedRectangle(cornerRadius: 22))
                }

                if let prediction = viewModel.prediction {
                    RiskCardView(prediction: prediction)
                }

                if let error = viewModel.errorMessage {
                    Text(error)
                        .font(.caption)
                        .foregroundStyle(.red)
                }
            }
            .padding(20)
            .padding(.bottom, 24)
        }
    }

    // MARK: - Settings Tab

    private var settingsTabContent: some View {
        ScrollView(showsIndicators: false) {
            VStack(alignment: .leading, spacing: 22) {
                VStack(alignment: .leading, spacing: 5) {
                    Text("Settings")
                        .font(.title2.bold())
                        .foregroundStyle(.white)

                    Text("About your environmental intelligence app")
                        .font(.subheadline)
                        .foregroundStyle(.white.opacity(0.55))
                }

                // App identity
                VStack(spacing: 12) {
                    Image(systemName: "leaf.fill")
                        .font(.system(size: 38))
                        .foregroundStyle(accentColor)
                        .frame(width: 76, height: 76)
                        .background(accentColor.opacity(0.12))
                        .clipShape(RoundedRectangle(cornerRadius: 22))

                    Text("AI Earth Guardian")
                        .font(.title3.bold())
                        .foregroundStyle(.white)

                    Text("AI-powered wildfire risk monitoring")
                        .font(.subheadline)
                        .foregroundStyle(.white.opacity(0.55))

                    Text("Version 1.0")
                        .font(.caption)
                        .foregroundStyle(accentColor)
                }
                .frame(maxWidth: .infinity)
                .padding(22)
                .background(cardColor)
                .clipShape(RoundedRectangle(cornerRadius: 22))

                settingsSection(title: "TECHNOLOGY") {
                    settingsRow(
                        icon: "brain.head.profile",
                        title: "Prediction Model",
                        subtitle: "XGBoost Machine Learning"
                    )

                    settingsDivider

                    settingsRow(
                        icon: "server.rack",
                        title: "Backend",
                        subtitle: "Python • FastAPI"
                    )

                    settingsDivider

                    settingsRow(
                        icon: "iphone",
                        title: "Mobile Application",
                        subtitle: "SwiftUI • MapKit • CoreLocation"
                    )
                }

                settingsSection(title: "DATA SOURCES") {
                    settingsRow(
                        icon: "flame.fill",
                        title: "NASA FIRMS",
                        subtitle: "Historical fire detections"
                    )

                    settingsDivider

                    settingsRow(
                        icon: "cloud.sun.fill",
                        title: "NASA POWER",
                        subtitle: "Historical weather observations"
                    )

                    settingsDivider

                    settingsRow(
                        icon: "cloud.fill",
                        title: "Open-Meteo",
                        subtitle: "Live weather information"
                    )
                }

                settingsSection(title: "PRIVACY & INFORMATION") {
                    settingsRow(
                        icon: "location.fill",
                        title: "Location Usage",
                        subtitle: "Used to estimate wildfire risk around your location"
                    )

                    settingsDivider

                    settingsRow(
                        icon: "shield.lefthalf.filled",
                        title: "Responsible Use",
                        subtitle: "Predictions are estimates, not official emergency alerts"
                    )
                }

                Text("AI Earth Guardian • Built for environmental monitoring")
                    .font(.caption2)
                    .foregroundStyle(.white.opacity(0.4))
                    .frame(maxWidth: .infinity)
                    .multilineTextAlignment(.center)
                    .padding(.vertical, 10)
            }
            .padding(20)
            .padding(.bottom, 24)
        }
    }

    // MARK: - Bottom Navigation

    private var bottomNavigation: some View {
        HStack(spacing: 0) {
            tabButton(title: "Home", icon: "house.fill")
            tabButton(title: "Map", icon: "map.fill")
            tabButton(title: "Insights", icon: "chart.bar.fill")
            tabButton(title: "Settings", icon: "gearshape.fill")
        }
        .padding(.top, 12)
        .padding(.bottom, 8)
        .background {
            cardColor
                .ignoresSafeArea(edges: .bottom)
                .overlay(alignment: .top) {
                    Rectangle()
                        .fill(.white.opacity(0.08))
                        .frame(height: 1)
                }
        }
    }

    private func tabButton(title: String, icon: String) -> some View {
        Button {
            withAnimation(.easeInOut(duration: 0.2)) {
                selectedTab = title
            }
        } label: {
            VStack(spacing: 6) {
                Image(systemName: icon)
                    .font(.system(size: 19, weight: .semibold))

                Text(title)
                    .font(.caption2.weight(.semibold))
            }
            .foregroundStyle(
                selectedTab == title
                ? accentColor
                : Color.white.opacity(0.45)
            )
            .frame(maxWidth: .infinity)
            .contentShape(Rectangle())
        }
        .buttonStyle(.plain)
    }

    // MARK: - Settings Reusable Components

    private func settingsSection<Content: View>(
        title: String,
        @ViewBuilder content: () -> Content
    ) -> some View {
        VStack(alignment: .leading, spacing: 12) {
            Text(title)
                .font(.caption2.weight(.bold))
                .tracking(1.2)
                .foregroundStyle(accentColor)

            VStack(spacing: 0) {
                content()
            }
            .padding(15)
            .background(cardColor)
            .clipShape(RoundedRectangle(cornerRadius: 20))
        }
    }

    private func settingsRow(
        icon: String,
        title: String,
        subtitle: String
    ) -> some View {
        HStack(alignment: .top, spacing: 12) {
            Image(systemName: icon)
                .font(.system(size: 18))
                .foregroundStyle(accentColor)
                .frame(width: 30)

            VStack(alignment: .leading, spacing: 4) {
                Text(title)
                    .font(.subheadline.weight(.semibold))
                    .foregroundStyle(.white)

                Text(subtitle)
                    .font(.caption)
                    .foregroundStyle(.white.opacity(0.55))
                    .fixedSize(horizontal: false, vertical: true)
            }

            Spacer(minLength: 0)
        }
        .padding(.vertical, 10)
    }

    private var settingsDivider: some View {
        Rectangle()
            .fill(.white.opacity(0.08))
            .frame(height: 1)
            .padding(.leading, 42)
    }

    // MARK: - Reusable UI

    private func sectionHeader(
        title: String,
        subtitle: String
    ) -> some View {
        VStack(alignment: .leading, spacing: 4) {
            Text(title)
                .font(.headline)
                .foregroundStyle(.white)

            Text(subtitle)
                .font(.caption)
                .foregroundStyle(.white.opacity(0.5))
        }
    }

    private var footerSection: some View {
        VStack(spacing: 6) {
            Text("POWERED BY AI + NASA DATA")
                .font(.caption2.weight(.bold))
                .tracking(1.2)
                .foregroundStyle(accentColor.opacity(0.8))

            Text("AI Earth Guardian • Wildfire Intelligence")
                .font(.caption2)
                .foregroundStyle(.white.opacity(0.4))
        }
        .frame(maxWidth: .infinity)
        .padding(.top, 8)
    }
}

// MARK: - Color Helper

private extension Color {
    init(hex: String) {
        let hex = hex.trimmingCharacters(
            in: CharacterSet.alphanumerics.inverted
        )
        let value = UInt64(hex, radix: 16) ?? 0

        self.init(
            .sRGB,
            red: Double((value >> 16) & 0xFF) / 255,
            green: Double((value >> 8) & 0xFF) / 255,
            blue: Double(value & 0xFF) / 255,
            opacity: 1
        )
    }
}

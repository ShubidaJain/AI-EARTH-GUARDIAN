
import SwiftUI
import MapKit
import CoreLocation

struct MapView: View {

    let location: CLLocation
    let gridPredictions: [GridPrediction]
    let gridRadius: Double
    let gridPoints: Int

    @State private var position: MapCameraPosition
    @State private var selectedPrediction: GridPrediction?

    private let backgroundColor = Color(hex: "102A22")
    private let accentColor = Color(hex: "75D69A")

    init(
        location: CLLocation,
        gridPredictions: [GridPrediction] = [],
        gridRadius: Double = 0.5,
        gridPoints: Int = 5
    ) {
        self.location = location
        self.gridPredictions = gridPredictions
        self.gridRadius = gridRadius
        self.gridPoints = gridPoints

        let region = MKCoordinateRegion(
            center: location.coordinate,
            latitudinalMeters: 100000,
            longitudinalMeters: 100000
        )

        _position = State(initialValue: .region(region))
    }

    // MARK: Grid Calculations

    private var cellSize: Double {
        guard gridPoints > 1 else { return 0 }
        return (2 * gridRadius) / Double(gridPoints - 1)
    }

    private var halfCell: Double {
        cellSize / 2
    }

    // MARK: Risk Colors

    private func riskColor(for level: String) -> Color {
        switch level.uppercased() {
        case "LOW":
            return Color(hex: "55D68B")
        case "MODERATE":
            return Color(hex: "F4D35E")
        case "HIGH":
            return Color(hex: "FF9F43")
        case "EXTREME":
            return Color(hex: "FF5C5C")
        default:
            return .gray
        }
    }

    // MARK: Map

    var body: some View {
        ZStack(alignment: .top) {

            Map(position: $position) {

                // User location
                Annotation(
                    "Your Location",
                    coordinate: location.coordinate
                ) {
                    UserLocationMarker()
                }

                // Grid polygons
                ForEach(gridPredictions) { prediction in

                    let latitude = prediction.location.latitude
                    let longitude = prediction.location.longitude
                    let half = halfCell

                    let coordinates = [
                        CLLocationCoordinate2D(
                            latitude: latitude + half,
                            longitude: longitude - half
                        ),
                        CLLocationCoordinate2D(
                            latitude: latitude + half,
                            longitude: longitude + half
                        ),
                        CLLocationCoordinate2D(
                            latitude: latitude - half,
                            longitude: longitude + half
                        ),
                        CLLocationCoordinate2D(
                            latitude: latitude - half,
                            longitude: longitude - half
                        )
                    ]

                    MapPolygon(coordinates: coordinates)
                        .foregroundStyle(
                            riskColor(
                                for: prediction.prediction.riskLevel
                            )
                            .opacity(0.30)
                        )
                        .stroke(
                            riskColor(
                                for: prediction.prediction.riskLevel
                            )
                            .opacity(0.85),
                            lineWidth: 1.5
                        )
                }

                // Risk markers
                ForEach(gridPredictions) { prediction in

                    Annotation(
                        prediction.prediction.riskLevel,
                        coordinate: CLLocationCoordinate2D(
                            latitude: prediction.location.latitude,
                            longitude: prediction.location.longitude
                        )
                    ) {
                        RiskMapMarker(
                            riskLevel: prediction.prediction.riskLevel,
                            probability: prediction.prediction.fireProbability
                        )
                        .onTapGesture {
                            selectedPrediction = prediction
                        }
                    }
                }
            }
            .mapStyle(
                .standard(
                    elevation: .flat,
                    emphasis: .muted
                )
            )
            .mapControls {
                MapCompass()
                MapScaleView()
            }

            // Top information bar
            HStack {
                HStack(spacing: 7) {
                    Circle()
                        .fill(accentColor)
                        .frame(width: 7, height: 7)

                    Text("LIVE RISK GRID")
                        .font(.caption2.weight(.bold))
                        .tracking(1)
                        .foregroundStyle(.white)
                }
                .padding(.horizontal, 12)
                .padding(.vertical, 10)
                .background(backgroundColor.opacity(0.95))
                .clipShape(Capsule())

                Spacer()

                Button {
                    recenterMap()
                } label: {
                    Image(systemName: "location.fill")
                        .font(.system(size: 15, weight: .bold))
                        .foregroundStyle(accentColor)
                        .frame(width: 38, height: 38)
                        .background(backgroundColor.opacity(0.95))
                        .clipShape(Circle())
                }
                .accessibilityLabel("Recenter map")
            }
            .padding(12)

            // Bottom legend
            VStack {
                Spacer()

                HStack {
                    RiskLegend()

                    Spacer()

                    if !gridPredictions.isEmpty {
                        Text("\(gridPredictions.count) CELLS")
                            .font(.caption2.weight(.bold))
                            .tracking(0.8)
                            .foregroundStyle(.white)
                            .padding(.horizontal, 11)
                            .padding(.vertical, 9)
                            .background(backgroundColor.opacity(0.95))
                            .clipShape(Capsule())
                    }
                }
                .padding(12)
            }

            // Empty grid state
            if gridPredictions.isEmpty {
                VStack(spacing: 8) {
                    Image(systemName: "map")
                        .font(.title2)
                        .foregroundStyle(accentColor)

                    Text("Waiting for regional predictions")
                        .font(.caption.weight(.medium))
                        .foregroundStyle(.white)
                }
                .padding(16)
                .background(backgroundColor.opacity(0.95))
                .clipShape(RoundedRectangle(cornerRadius: 16))
            }
        }
        .clipShape(RoundedRectangle(cornerRadius: 20))
        .sheet(item: $selectedPrediction) { prediction in
            RiskDetailView(prediction: prediction)
        }
    }

    // MARK: Recenter

    private func recenterMap() {
        let region = MKCoordinateRegion(
            center: location.coordinate,
            latitudinalMeters: 100000,
            longitudinalMeters: 100000
        )

        withAnimation {
            position = .region(region)
        }
    }
}

// MARK: User Location Marker

struct UserLocationMarker: View {

    var body: some View {
        ZStack {
            Circle()
                .fill(Color.blue.opacity(0.20))
                .frame(width: 42, height: 42)

            Circle()
                .fill(Color.blue)
                .frame(width: 19, height: 19)

            Circle()
                .stroke(.white, lineWidth: 3)
                .frame(width: 19, height: 19)
        }
    }
}

// MARK: Risk Marker

struct RiskMapMarker: View {

    let riskLevel: String
    let probability: Double

    private var markerColor: Color {
        switch riskLevel.uppercased() {
        case "LOW":
            return Color(hex: "55D68B")
        case "MODERATE":
            return Color(hex: "F4D35E")
        case "HIGH":
            return Color(hex: "FF9F43")
        case "EXTREME":
            return Color(hex: "FF5C5C")
        default:
            return .gray
        }
    }

    var body: some View {
        VStack(spacing: 3) {
            ZStack {
                Circle()
                    .fill(markerColor.opacity(0.25))
                    .frame(width: 35, height: 35)

                Circle()
                    .fill(markerColor)
                    .frame(width: 17, height: 17)

                Circle()
                    .stroke(.white, lineWidth: 2)
                    .frame(width: 17, height: 17)
            }

            Text("\(Int(probability * 100))%")
                .font(.system(size: 9, weight: .bold))
                .foregroundStyle(.white)
                .padding(.horizontal, 5)
                .padding(.vertical, 3)
                .background(Color(hex: "102A22").opacity(0.95))
                .clipShape(Capsule())
        }
    }
}

// MARK: Risk Legend

struct RiskLegend: View {

    var body: some View {
        VStack(alignment: .leading, spacing: 8) {

            Text("FIRE RISK")
                .font(.caption2.weight(.bold))
                .tracking(1)
                .foregroundStyle(.white)

            RiskLegendRow(
                color: Color(hex: "55D68B"),
                text: "Low"
            )

            RiskLegendRow(
                color: Color(hex: "F4D35E"),
                text: "Moderate"
            )

            RiskLegendRow(
                color: Color(hex: "FF9F43"),
                text: "High"
            )

            RiskLegendRow(
                color: Color(hex: "FF5C5C"),
                text: "Extreme"
            )
        }
        .padding(12)
        .background(Color(hex: "102A22").opacity(0.96))
        .clipShape(RoundedRectangle(cornerRadius: 14))
        .overlay {
            RoundedRectangle(cornerRadius: 14)
                .stroke(.white.opacity(0.1), lineWidth: 1)
        }
    }
}

struct RiskLegendRow: View {

    let color: Color
    let text: String

    var body: some View {
        HStack(spacing: 8) {
            Circle()
                .fill(color)
                .frame(width: 8, height: 8)

            Text(text)
                .font(.caption2)
                .foregroundStyle(.white.opacity(0.8))
        }
    }
}

// MARK: Color Helper

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

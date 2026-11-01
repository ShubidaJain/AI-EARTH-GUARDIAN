
import SwiftUI

struct RiskDetailView: View {

    let prediction: GridPrediction

    private let backgroundColor = Color(hex: "071B16")
    private let cardColor = Color(hex: "102A22")
    private let accentColor = Color(hex: "75D69A")

    private var riskLevel: String {
        prediction.prediction.riskLevel.uppercased()
    }

    private var probability: Double {
        min(max(prediction.prediction.fireProbability, 0), 1)
    }

    private var probabilityPercentage: Int {
        Int(probability * 100)
    }

    private var riskColor: Color {
        switch riskLevel {
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
        NavigationStack {
            ZStack {
                backgroundColor
                    .ignoresSafeArea()

                ScrollView(showsIndicators: false) {
                    VStack(alignment: .leading, spacing: 20) {

                        riskOverview

                        currentWeatherSection

                        historicalWeatherSection

                        locationSection

                        modelInformation
                    }
                    .padding(20)
                    .padding(.bottom, 24)
                }
            }
            .navigationTitle("Risk Details")
            .navigationBarTitleDisplayMode(.inline)
            .toolbarColorScheme(.dark, for: .navigationBar)
            .toolbarBackground(backgroundColor, for: .navigationBar)
            .toolbarBackground(.visible, for: .navigationBar)
        }
        .preferredColorScheme(.dark)
    }

    // MARK: Risk Overview

    private var riskOverview: some View {
        VStack(spacing: 18) {

            HStack {
                Text("GRID CELL ASSESSMENT")
                    .font(.caption2.weight(.bold))
                    .tracking(1.3)
                    .foregroundStyle(.white.opacity(0.55))

                Spacer()

                Image(systemName: "flame.fill")
                    .foregroundStyle(riskColor)
            }

            ZStack {
                Circle()
                    .stroke(.white.opacity(0.08), lineWidth: 12)

                Circle()
                    .trim(from: 0, to: probability)
                    .stroke(
                        riskColor,
                        style: StrokeStyle(
                            lineWidth: 12,
                            lineCap: .round
                        )
                    )
                    .rotationEffect(.degrees(-90))

                VStack(spacing: 3) {
                    Text("\(probabilityPercentage)%")
                        .font(.system(size: 37, weight: .bold, design: .rounded))
                        .foregroundStyle(.white)

                    Text("PROBABILITY")
                        .font(.system(size: 9, weight: .bold))
                        .tracking(1)
                        .foregroundStyle(.white.opacity(0.5))
                }
            }
            .frame(width: 145, height: 145)
            .padding(.vertical, 8)

            Text(riskLevel)
                .font(.title2.bold())
                .tracking(1.5)
                .foregroundStyle(riskColor)

            Text("Predicted wildfire risk for this grid location")
                .font(.subheadline)
                .foregroundStyle(.white.opacity(0.55))
                .multilineTextAlignment(.center)
        }
        .frame(maxWidth: .infinity)
        .padding(22)
        .background(cardColor)
        .clipShape(RoundedRectangle(cornerRadius: 24))
        .overlay {
            RoundedRectangle(cornerRadius: 24)
                .stroke(riskColor.opacity(0.25), lineWidth: 1)
        }
    }

    // MARK: Current Weather

    private var currentWeatherSection: some View {
        VStack(alignment: .leading, spacing: 16) {

            sectionHeader(
                title: "Current Weather",
                subtitle: "Environmental conditions at this grid cell",
                icon: "cloud.sun.fill"
            )

            LazyVGrid(
                columns: [
                    GridItem(.flexible()),
                    GridItem(.flexible())
                ],
                spacing: 12
            ) {
                metricCard(
                    icon: "thermometer.medium",
                    title: "Temperature",
                    value: String(
                        format: "%.1f °C",
                        prediction.weather.temperature
                    )
                )

                metricCard(
                    icon: "humidity.fill",
                    title: "Humidity",
                    value: String(
                        format: "%.1f%%",
                        prediction.weather.humidity
                    )
                )

                metricCard(
                    icon: "wind",
                    title: "Wind Speed",
                    value: String(
                        format: "%.1f m/s",
                        prediction.weather.windSpeed
                    )
                )

                metricCard(
                    icon: "cloud.rain.fill",
                    title: "Rainfall",
                    value: String(
                        format: "%.1f mm",
                        prediction.weather.rainfall
                    )
                )
            }
        }
    }

    // MARK: Historical Weather

    private var historicalWeatherSection: some View {
        VStack(alignment: .leading, spacing: 16) {

            sectionHeader(
                title: "Historical Conditions",
                subtitle: "Recent weather patterns used by the model",
                icon: "chart.xyaxis.line"
            )

            VStack(spacing: 0) {

                historicalRow(
                    icon: "thermometer.medium",
                    title: "3-Day Avg. Temperature",
                    value: String(
                        format: "%.1f °C",
                        prediction.historicalWeather.temperature3dMean
                    )
                )

                divider

                historicalRow(
                    icon: "thermometer.medium",
                    title: "7-Day Avg. Temperature",
                    value: String(
                        format: "%.1f °C",
                        prediction.historicalWeather.temperature7dMean
                    )
                )

                divider

                historicalRow(
                    icon: "wind",
                    title: "7-Day Avg. Wind",
                    value: String(
                        format: "%.1f m/s",
                        prediction.historicalWeather.wind7dMean
                    )
                )

                divider

                historicalRow(
                    icon: "cloud.rain.fill",
                    title: "7-Day Total Rainfall",
                    value: String(
                        format: "%.1f mm",
                        prediction.historicalWeather.rainfall7dSum
                    )
                )
            }
        }
        .padding(18)
        .background(cardColor)
        .clipShape(RoundedRectangle(cornerRadius: 22))
    }

    // MARK: Grid Location

    private var locationSection: some View {
        VStack(alignment: .leading, spacing: 15) {

            sectionHeader(
                title: "Grid Location",
                subtitle: "Geographic coordinates of this prediction",
                icon: "location.fill"
            )

            coordinateRow(
                title: "Latitude",
                value: String(
                    format: "%.4f",
                    prediction.location.latitude
                )
            )

            coordinateRow(
                title: "Longitude",
                value: String(
                    format: "%.4f",
                    prediction.location.longitude
                )
            )

            divider

            coordinateRow(
                title: "Model Grid Latitude",
                value: String(
                    format: "%.4f",
                    prediction.location.gridLat
                )
            )

            coordinateRow(
                title: "Model Grid Longitude",
                value: String(
                    format: "%.4f",
                    prediction.location.gridLon
                )
            )
        }
        .padding(18)
        .background(cardColor)
        .clipShape(RoundedRectangle(cornerRadius: 22))
    }

    // MARK: Model Information

    private var modelInformation: some View {
        HStack(alignment: .top, spacing: 12) {
            Image(systemName: "brain.head.profile")
                .font(.title2)
                .foregroundStyle(accentColor)

            VStack(alignment: .leading, spacing: 5) {
                Text("AI-Powered Assessment")
                    .font(.subheadline.bold())
                    .foregroundStyle(.white)

                Text("This prediction is generated using environmental and historical weather features processed by the wildfire risk model.")
                    .font(.caption)
                    .foregroundStyle(.white.opacity(0.55))
                    .fixedSize(horizontal: false, vertical: true)
            }
        }
        .padding(17)
        .frame(maxWidth: .infinity, alignment: .leading)
        .background(accentColor.opacity(0.09))
        .clipShape(RoundedRectangle(cornerRadius: 18))
    }

    // MARK: Reusable Components

    private func sectionHeader(
        title: String,
        subtitle: String,
        icon: String
    ) -> some View {
        HStack(spacing: 10) {
            Image(systemName: icon)
                .font(.system(size: 18))
                .foregroundStyle(accentColor)

            VStack(alignment: .leading, spacing: 4) {
                Text(title)
                    .font(.headline)
                    .foregroundStyle(.white)

                Text(subtitle)
                    .font(.caption)
                    .foregroundStyle(.white.opacity(0.5))
            }
        }
    }

    private func metricCard(
        icon: String,
        title: String,
        value: String
    ) -> some View {
        VStack(alignment: .leading, spacing: 12) {
            Image(systemName: icon)
                .font(.system(size: 18))
                .foregroundStyle(accentColor)

            Text(value)
                .font(.title3.bold())
                .foregroundStyle(.white)

            Text(title)
                .font(.caption)
                .foregroundStyle(.white.opacity(0.55))
        }
        .frame(maxWidth: .infinity, alignment: .leading)
        .padding(15)
        .background(cardColor)
        .clipShape(RoundedRectangle(cornerRadius: 17))
    }

    private func historicalRow(
        icon: String,
        title: String,
        value: String
    ) -> some View {
        HStack(spacing: 12) {
            Image(systemName: icon)
                .foregroundStyle(accentColor)
                .frame(width: 25)

            Text(title)
                .font(.subheadline)
                .foregroundStyle(.white.opacity(0.7))

            Spacer()

            Text(value)
                .font(.subheadline.bold())
                .foregroundStyle(.white)
        }
        .padding(.vertical, 12)
    }

    private func coordinateRow(
        title: String,
        value: String
    ) -> some View {
        HStack {
            Text(title)
                .font(.subheadline)
                .foregroundStyle(.white.opacity(0.6))

            Spacer()

            Text(value)
                .font(.subheadline.monospaced().weight(.semibold))
                .foregroundStyle(.white)
        }
    }

    private var divider: some View {
        Rectangle()
            .fill(.white.opacity(0.08))
            .frame(height: 1)
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

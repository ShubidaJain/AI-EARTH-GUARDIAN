
import SwiftUI

struct RiskCardView: View {

    let prediction: PredictionResponse

    private var probability: Int {
        Int(prediction.prediction.fireProbability * 100)
    }

    private var riskLevel: String {
        prediction.prediction.riskLevel.uppercased()
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
            return Color(hex: "75D69A")
        }
    }

    var body: some View {
        VStack(alignment: .leading, spacing: 22) {

            // Header
            HStack {
                VStack(alignment: .leading, spacing: 5) {
                    Text("CURRENT ASSESSMENT")
                        .font(.caption2.weight(.bold))
                        .tracking(1.3)
                        .foregroundStyle(.white.opacity(0.55))

                    Text("Wildfire Risk")
                        .font(.title2.bold())
                        .foregroundStyle(.white)
                }

                Spacer()

                Image(systemName: "flame.fill")
                    .font(.system(size: 25))
                    .foregroundStyle(riskColor)
                    .frame(width: 52, height: 52)
                    .background(riskColor.opacity(0.13))
                    .clipShape(RoundedRectangle(cornerRadius: 16))
            }

            // Probability
            HStack(alignment: .center, spacing: 18) {
                VStack(alignment: .leading, spacing: 4) {
                    Text("\(probability)%")
                        .font(.system(size: 48, weight: .bold, design: .rounded))
                        .foregroundStyle(.white)
                        .contentTransition(.numericText())

                    Text("Fire probability")
                        .font(.subheadline)
                        .foregroundStyle(.white.opacity(0.55))
                }

                Spacer()

                VStack(alignment: .trailing, spacing: 8) {
                    Text(riskLevel)
                        .font(.subheadline.weight(.bold))
                        .tracking(1)
                        .foregroundStyle(riskColor)
                        .padding(.horizontal, 14)
                        .padding(.vertical, 9)
                        .background(riskColor.opacity(0.14))
                        .clipShape(Capsule())

                    Text("AI risk classification")
                        .font(.caption2)
                        .foregroundStyle(.white.opacity(0.45))
                }
            }

            // Probability bar
            VStack(alignment: .leading, spacing: 8) {
                GeometryReader { geometry in
                    ZStack(alignment: .leading) {
                        Capsule()
                            .fill(.white.opacity(0.09))

                        Capsule()
                            .fill(riskColor)
                            .frame(
                                width: geometry.size.width *
                                CGFloat(min(max(probability, 0), 100)) / 100
                            )
                    }
                }
                .frame(height: 9)

                HStack {
                    Text("0%")
                    Spacer()
                    Text("100%")
                }
                .font(.caption2)
                .foregroundStyle(.white.opacity(0.4))
            }

            Rectangle()
                .fill(.white.opacity(0.09))
                .frame(height: 1)

            // Weather information
            Text("CURRENT CONDITIONS")
                .font(.caption2.weight(.bold))
                .tracking(1.2)
                .foregroundStyle(.white.opacity(0.55))

            LazyVGrid(
                columns: [
                    GridItem(.flexible()),
                    GridItem(.flexible())
                ],
                spacing: 16
            ) {
                weatherItem(
                    icon: "thermometer.medium",
                    title: "Temperature",
                    value: String(format: "%.1f °C", prediction.weather.temperature)
                )

                weatherItem(
                    icon: "humidity.fill",
                    title: "Humidity",
                    value: String(format: "%.1f%%", prediction.weather.humidity)
                )

                weatherItem(
                    icon: "wind",
                    title: "Wind speed",
                    value: String(format: "%.1f m/s", prediction.weather.windSpeed)
                )

                weatherItem(
                    icon: "cloud.rain.fill",
                    title: "Rainfall",
                    value: String(format: "%.1f mm", prediction.weather.rainfall)
                )
            }
        }
        .padding(20)
        .frame(maxWidth: .infinity, alignment: .leading)
        .background(Color(hex: "102A22"))
        .clipShape(RoundedRectangle(cornerRadius: 24))
        .overlay {
            RoundedRectangle(cornerRadius: 24)
                .stroke(.white.opacity(0.08), lineWidth: 1)
        }
    }

    private func weatherItem(
        icon: String,
        title: String,
        value: String
    ) -> some View {
        HStack(spacing: 10) {
            Image(systemName: icon)
                .font(.system(size: 17))
                .foregroundStyle(Color(hex: "75D69A"))
                .frame(width: 34, height: 34)
                .background(Color(hex: "75D69A").opacity(0.12))
                .clipShape(RoundedRectangle(cornerRadius: 10))

            VStack(alignment: .leading, spacing: 3) {
                Text(title)
                    .font(.caption)
                    .foregroundStyle(.white.opacity(0.5))

                Text(value)
                    .font(.subheadline.weight(.semibold))
                    .foregroundStyle(.white)
            }

            Spacer(minLength: 0)
        }
    }
}

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

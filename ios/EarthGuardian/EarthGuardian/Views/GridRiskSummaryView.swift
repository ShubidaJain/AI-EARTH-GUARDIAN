
import SwiftUI

struct GridRiskSummaryView: View {

    let predictions: [GridPrediction]

    private var averageProbability: Double {
        guard !predictions.isEmpty else { return 0 }

        return predictions
            .map { $0.prediction.fireProbability }
            .reduce(0, +) / Double(predictions.count)
    }

    private var highestProbability: Double {
        predictions
            .map { $0.prediction.fireProbability }
            .max() ?? 0
    }

    private func count(for level: String) -> Int {
        predictions.filter {
            $0.prediction.riskLevel.uppercased() == level
        }.count
    }

    private var highRiskCount: Int {
        count(for: "HIGH") + count(for: "EXTREME")
    }

    var body: some View {
        VStack(alignment: .leading, spacing: 20) {

            // Heading
            VStack(alignment: .leading, spacing: 5) {
                HStack(spacing: 9) {
                    Image(systemName: "chart.bar.xaxis")
                        .foregroundStyle(Color(hex: "75D69A"))

                    Text("Regional Risk Analysis")
                        .font(.headline)
                        .foregroundStyle(.white)
                }

                Text("\(predictions.count) monitored grid locations")
                    .font(.caption)
                    .foregroundStyle(.white.opacity(0.5))
            }

            // Statistics
            HStack(spacing: 10) {
                RiskStatistic(
                    title: "Average",
                    value: "\(Int(averageProbability * 100))%",
                    icon: "chart.line.uptrend.xyaxis",
                    color: Color(hex: "75D69A")
                )

                RiskStatistic(
                    title: "Highest",
                    value: "\(Int(highestProbability * 100))%",
                    icon: "arrow.up.right",
                    color: Color(hex: "FF9F43")
                )

                RiskStatistic(
                    title: "High Risk",
                    value: "\(highRiskCount)",
                    icon: "flame.fill",
                    color: Color(hex: "FF5C5C")
                )
            }

            Rectangle()
                .fill(.white.opacity(0.09))
                .frame(height: 1)

            // Risk distribution
            Text("RISK DISTRIBUTION")
                .font(.caption2.weight(.bold))
                .tracking(1.2)
                .foregroundStyle(.white.opacity(0.55))

            VStack(spacing: 15) {
                distributionRow(
                    title: "Low",
                    level: "LOW",
                    color: Color(hex: "55D68B")
                )

                distributionRow(
                    title: "Moderate",
                    level: "MODERATE",
                    color: Color(hex: "F4D35E")
                )

                distributionRow(
                    title: "High",
                    level: "HIGH",
                    color: Color(hex: "FF9F43")
                )

                distributionRow(
                    title: "Extreme",
                    level: "EXTREME",
                    color: Color(hex: "FF5C5C")
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

    private func distributionRow(
        title: String,
        level: String,
        color: Color
    ) -> some View {

        let total = predictions.count
        let riskCount = count(for: level)

        let fraction = total > 0
            ? CGFloat(riskCount) / CGFloat(total)
            : 0

        return VStack(spacing: 7) {
            HStack {
                HStack(spacing: 8) {
                    Circle()
                        .fill(color)
                        .frame(width: 8, height: 8)

                    Text(title)
                        .font(.subheadline)
                        .foregroundStyle(.white.opacity(0.8))
                }

                Spacer()

                Text("\(riskCount) / \(total)")
                    .font(.caption.weight(.semibold).monospacedDigit())
                    .foregroundStyle(.white.opacity(0.7))
            }

            GeometryReader { geometry in
                ZStack(alignment: .leading) {
                    Capsule()
                        .fill(.white.opacity(0.08))

                    Capsule()
                        .fill(color)
                        .frame(width: geometry.size.width * fraction)
                }
            }
            .frame(height: 7)
        }
    }
}

struct RiskStatistic: View {

    let title: String
    let value: String
    let icon: String
    let color: Color

    var body: some View {
        VStack(alignment: .leading, spacing: 10) {
            Image(systemName: icon)
                .font(.system(size: 15))
                .foregroundStyle(color)

            Text(value)
                .font(.system(size: 22, weight: .bold, design: .rounded))
                .foregroundStyle(.white)
                .minimumScaleFactor(0.7)
                .lineLimit(1)

            Text(title)
                .font(.caption2)
                .foregroundStyle(.white.opacity(0.55))
                .lineLimit(1)
        }
        .frame(maxWidth: .infinity, alignment: .leading)
        .padding(12)
        .background(Color(hex: "17372C"))
        .clipShape(RoundedRectangle(cornerRadius: 15))
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

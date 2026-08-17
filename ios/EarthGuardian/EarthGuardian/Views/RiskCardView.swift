import SwiftUI

struct RiskCardView: View {

    let prediction: PredictionResponse

    private var probability: Int {
        Int(
            prediction.prediction.fireProbability * 100
        )
    }

    var body: some View {

        VStack(spacing: 16) {

            HStack {

                Text("🔥 Fire Risk")
                    .font(.title2)
                    .bold()

                Spacer()

                Text(
                    prediction.prediction.riskLevel
                )
                .bold()
            }

            HStack {

                VStack(
                    alignment: .leading
                ) {

                    Text("\(probability)%")
                        .font(
                            .system(
                                size: 42,
                                weight: .bold
                            )
                        )

                    Text("Probability")
                        .foregroundStyle(
                            .secondary
                        )
                }

                Spacer()

                VStack(
                    alignment: .trailing
                ) {

                    Text(
                        "🌡️ \(prediction.weather.temperature, specifier: "%.1f")°C"
                    )

                    Text(
                        "💧 \(prediction.weather.humidity, specifier: "%.1f")%"
                    )

                    Text(
                        "💨 \(prediction.weather.windSpeed, specifier: "%.1f") m/s"
                    )

                    Text(
                        "🌧️ \(prediction.weather.rainfall, specifier: "%.1f") mm"
                    )
                }
            }
        }
        .padding()
        .background(
            RoundedRectangle(
                cornerRadius: 20
            )
            .fill(
                Color(.secondarySystemBackground)
            )
        )
    }
}

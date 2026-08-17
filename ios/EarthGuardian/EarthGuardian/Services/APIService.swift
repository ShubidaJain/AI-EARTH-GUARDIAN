import Foundation

final class APIService {

    static let shared = APIService()

    private init() {}

    func predictLive(
        latitude: Double,
        longitude: Double
    ) async throws -> PredictionResponse {

        let urlString =
            "http://172.25.43.243:8000/predict/live"

        guard let url = URL(string: urlString) else {
            throw URLError(.badURL)
        }

        var request = URLRequest(url: url)

        request.httpMethod = "POST"

        request.setValue(
            "application/json",
            forHTTPHeaderField: "Content-Type"
        )

        let body: [String: Double] = [
            "latitude": latitude,
            "longitude": longitude
        ]

        request.httpBody = try JSONSerialization.data(
            withJSONObject: body
        )

        let (data, response) =
            try await URLSession.shared.data(
                for: request
            )

        guard let httpResponse =
                response as? HTTPURLResponse else {
            throw URLError(.badServerResponse)
        }

        guard 200..<300 ~= httpResponse.statusCode else {

            print(
                "HTTP Status:",
                httpResponse.statusCode
            )

            print(
                String(
                    data: data,
                    encoding: .utf8
                ) ?? "No response"
            )

            throw URLError(.badServerResponse)
        }

        return try JSONDecoder().decode(
            PredictionResponse.self,
            from: data
        )
    }
}

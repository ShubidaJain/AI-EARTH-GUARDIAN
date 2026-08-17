import SwiftUI
import MapKit
import CoreLocation

struct MapView: View {

    let location: CLLocation

    @State private var position: MapCameraPosition

    init(location: CLLocation) {

        self.location = location

        let region = MKCoordinateRegion(
            center: location.coordinate,
            latitudinalMeters: 5000,
            longitudinalMeters: 5000
        )

        _position = State(
            initialValue: .region(region)
        )
    }

    var body: some View {

        Map(position: $position) {

            Annotation(
                "You",
                coordinate: location.coordinate
            ) {

                ZStack {

                    Circle()
                        .fill(.blue)
                        .frame(
                            width: 22,
                            height: 22
                        )

                    Circle()
                        .stroke(
                            .white,
                            lineWidth: 3
                        )
                }
            }
        }
        .clipShape(
            RoundedRectangle(
                cornerRadius: 20
            )
        )
    }
}

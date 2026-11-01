//
//  SplashView.swift
//  EarthGuardian
//
//  Created by Priyanshu Patel on 01/11/26.
//


import SwiftUI

struct SplashView: View {

    @State private var animateLogo = false

    private let accentColor = Color(
        red: 117 / 255,
        green: 214 / 255,
        blue: 154 / 255
    )

    var body: some View {
        ZStack {
            LinearGradient(
                colors: [
                    Color(red: 4 / 255, green: 25 / 255, blue: 18 / 255),
                    Color(red: 7 / 255, green: 45 / 255, blue: 30 / 255),
                    Color(red: 3 / 255, green: 18 / 255, blue: 14 / 255)
                ],
                startPoint: .topLeading,
                endPoint: .bottomTrailing
            )
            .ignoresSafeArea()

            Circle()
                .fill(accentColor.opacity(0.12))
                .frame(width: 260, height: 260)
                .blur(radius: 70)

            VStack(spacing: 22) {

                ZStack {
                    Circle()
                        .stroke(
                            accentColor.opacity(0.25),
                            lineWidth: 1
                        )
                        .frame(width: 170, height: 170)

                    Circle()
                        .fill(accentColor.opacity(0.12))
                        .frame(width: 140, height: 140)

                    Image(systemName: "globe.americas.fill")
                        .font(.system(size: 100))
                        .foregroundStyle(accentColor.opacity(0.9))

                    Image(systemName: "leaf.fill")
                        .font(.system(size: 48))
                        .foregroundStyle(.white)
                        .offset(x: 28, y: 32)
                }
                .scaleEffect(animateLogo ? 1 : 0.75)
                .opacity(animateLogo ? 1 : 0)

                VStack(spacing: 8) {
                    Text("EARTH GUARDIAN")
                        .font(
                            .system(
                                size: 25,
                                weight: .bold,
                                design: .rounded
                            )
                        )
                        .tracking(2)
                        .foregroundStyle(.white)

                    Text("AI-POWERED WILDFIRE INTELLIGENCE")
                        .font(.system(size: 10, weight: .semibold))
                        .tracking(2)
                        .foregroundStyle(accentColor)
                }
                .opacity(animateLogo ? 1 : 0)
                .offset(y: animateLogo ? 0 : 12)

                ProgressView()
                    .tint(accentColor)
                    .padding(.top, 20)
                    .opacity(animateLogo ? 1 : 0)
            }
        }
        .onAppear {
            withAnimation(.easeOut(duration: 0.9)) {
                animateLogo = true
            }
        }
        .preferredColorScheme(.dark)
    }
}

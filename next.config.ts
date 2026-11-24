import type { NextConfig } from "next";

const nextConfig: NextConfig = {
  output: "standalone",
  /* config options here */
  typescript: {
    ignoreBuildErrors: true,
  },
  reactStrictMode: false,
  async rewrites() {
    return {
      beforeFiles: [
        // Serve the static Garage Build Library landing page at the root URL.
        { source: "/", destination: "/site.html" },
      ],
      afterFiles: [],
      fallback: [],
    };
  },
};

export default nextConfig;

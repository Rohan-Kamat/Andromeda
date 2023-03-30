/** @type {import('next').NextConfig} */
const nextConfig = {
  reactStrictMode: true,
  publicRuntimeConfig: {
    apiHost: 'http://10.22.0.51:5000',
    perPage: 10,
  },
  images: {
    domains: ['www.google.com'],
    unoptimized: true,
  }
}

module.exports = nextConfig

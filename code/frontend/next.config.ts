import type { NextConfig } from "next";
import path from "path";

const nextConfig: NextConfig = {
  // 让 Vercel 把 gpt/prompts/ 也打包进 serverless function
  outputFileTracingRoot: path.join(__dirname, "../../"),
  outputFileTracingIncludes: {
    "/api/dig/layer1": ["../../gpt/prompts/**"],
    "/api/dig/layer2": ["../../gpt/prompts/**"],
    "/api/dig/stocks": ["../../gpt/prompts/**"],
  },
};

export default nextConfig;

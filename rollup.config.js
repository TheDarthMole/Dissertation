import {nodeResolve} from "@rollup/plugin-node-resolve"
export default {
  input: "./apps/static/assets/js/editor.js",
  output: {
    file: "./apps/static/assets/js/editor.bundle.js",
    format: "iife"
  },
  plugins: [nodeResolve()]
}
const { createDefaultPreset } = require("ts-jest");

const tsJestTransformCfg = createDefaultPreset().transform;

/** @type {import("jest").Config} **/
module.exports = {
  testEnvironment: "node",
  testMatch: [
    "**/?(*.)+(test|spec|Test).[tj]s?(x)",
    "**/__tests__/**/*.[tj]s?(x)",
  ],
  transform: {
    ...tsJestTransformCfg,
  },
};
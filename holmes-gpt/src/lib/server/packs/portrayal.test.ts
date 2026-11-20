import { describe, expect, it } from "vitest";
import { withPortrayalLabel } from "$lib/portrayal";
import { HOLMES_COMPACT_PROMPT, HOLMES_SYSTEM_PROMPT } from "../prompts";
import { CRISIS_NOTE, detectCrisis, portrayalRules } from "./portrayal";

describe("portrayal rules", () => {
  const rules = portrayalRules("Ernest Holmes");

  it("names the teacher and says the portrayal is not them", () => {
    expect(rules).toContain("AI portrayal of Ernest Holmes");
    expect(rules).toContain("you are not Ernest Holmes");
  });

  it("covers the policy points the prompt can enforce", () => {
    for (const phrase of [
      "Never present wording you are composing as a quotation",
      "goes beyond anything",
      "Never endorse",
      "Never suggest skipping, delaying or stopping medical treatment",
      "historical context",
      "mocking, sexual or degrading",
    ]) {
      expect(rules).toContain(phrase);
    }
  });

  it("no longer tells the model it is the man himself", () => {
    expect(HOLMES_SYSTEM_PROMPT).not.toMatch(/You ARE Ernest Holmes/);
    expect(HOLMES_SYSTEM_PROMPT).toContain("AI portrayal of Ernest Holmes");
    expect(HOLMES_COMPACT_PROMPT).toContain("not the man himself");
  });
});

describe("crisis detection", () => {
  it.each([
    "I want to die",
    "Sometimes I think about suicide",
    "I've been hurting myself again",
    "I don't want to live anymore",
    "everyone would be better off dead without me",
    "I took an overdose last year",
    "he hits me when he drinks",
  ])("fires on %j", (text) => {
    expect(detectCrisis(text)).toBe(true);
  });

  it.each([
    "How do I pray in the Science of Mind way?",
    "What did you teach about death and the afterlife?",
    "Help me let go of fear",
    "My work is killing me, how do I find peace?",
  ])("stays quiet on %j", (text) => {
    expect(detectCrisis(text)).toBe(false);
  });

  it("checks every text it is given, not only the first", () => {
    expect(detectCrisis("thank you", "earlier I said I want to die")).toBe(
      true,
    );
  });

  it("points to real help", () => {
    expect(CRISIS_NOTE).toContain("988");
    expect(CRISIS_NOTE).toContain("emergency number");
  });
});

describe("shared text", () => {
  it("carries the portrayal label", () => {
    const shared = withPortrayalLabel("Know that you are whole.");
    expect(shared).toMatch(/^Know that you are whole\.\n\n\(An AI portrayal/);
    expect(shared).toContain("not medical advice");
  });
});

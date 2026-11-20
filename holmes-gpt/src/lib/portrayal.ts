// Client-safe labels for the AI portrayal (teacher policy §3). The full pack
// lives server-side; until the teacher picker lands, Holmes is the only one.

export const TEACHER_NAME = "Ernest Holmes";

/** Short label shown above every answer. */
export const PORTRAYAL_EYEBROW = `AI portrayal of ${TEACHER_NAME}`;

/** One-line notice under the composer and on anything shared. */
export const PORTRAYAL_NOTICE = `An AI portrayal of ${TEACHER_NAME}, based on his published teaching. Not ${TEACHER_NAME}, and not medical advice.`;

/** Appended to text that leaves the app (copy, email), so the label travels with it. */
export function withPortrayalLabel(text: string): string {
  return `${text.trimEnd()}\n\n(${PORTRAYAL_NOTICE})`;
}

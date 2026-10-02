/**
 * Shows generation speed (output tokens per second) in the footer after each
 * assistant message. Timing starts at the first streamed token, so prompt
 * processing time is excluded.
 */

import type { ExtensionAPI } from "@earendil-works/pi-coding-agent";

export default function (pi: ExtensionAPI) {
	let firstTokenAt: number | undefined;

	pi.on("message_start", async () => {
		firstTokenAt = undefined;
	});

	pi.on("message_update", async (event) => {
		if (firstTokenAt === undefined && event.assistantMessageEvent.type.endsWith("_delta")) {
			firstTokenAt = performance.now();
		}
	});

	pi.on("message_end", async (event, ctx) => {
		const message = event.message;
		if (message.role !== "assistant" || firstTokenAt === undefined) return;

		const seconds = (performance.now() - firstTokenAt) / 1000;
		const tokens = message.usage?.output ?? 0;
		firstTokenAt = undefined;
		if (tokens === 0 || seconds <= 0) return;

		const theme = ctx.ui.theme;
		ctx.ui.setStatus("tps", theme.fg("dim", `${(tokens / seconds).toFixed(1)} tok/s`));
	});
}

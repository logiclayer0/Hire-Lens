import { scoreColor } from "@/lib/utils";

export function ScoreBadge({ score }: { score: number }) {
  return (
    <div className="flex items-baseline gap-1">
      <span className={`text-2xl font-bold ${scoreColor(score)}`}>
        {score.toFixed(0)}
      </span>
      <span className="text-xs text-slate-500">/100</span>
    </div>
  );
}
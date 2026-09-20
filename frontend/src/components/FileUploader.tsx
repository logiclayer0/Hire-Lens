"use client";

import { useRef, useState } from "react";
import { UploadCloud, FileText, X } from "lucide-react";
import { cn } from "@/lib/utils";

export function FileUploader({
  label,
  multiple = false,
  files,
  onChange,
}: {
  label: string;
  multiple?: boolean;
  files: File[];
  onChange: (files: File[]) => void;
}) {
  const inputRef = useRef<HTMLInputElement>(null);
  const [drag, setDrag] = useState(false);

  function handleFiles(list: FileList | null) {
    if (!list) return;
    const arr = Array.from(list);
    onChange(multiple ? [...files, ...arr] : arr.slice(0, 1));
  }

  return (
    <div>
      <div
        onDragOver={(e) => {
          e.preventDefault();
          setDrag(true);
        }}
        onDragLeave={() => setDrag(false)}
        onDrop={(e) => {
          e.preventDefault();
          setDrag(false);
          handleFiles(e.dataTransfer.files);
        }}
        onClick={() => inputRef.current?.click()}
        className={cn(
          "cursor-pointer rounded-xl border-2 border-dashed p-8 text-center transition",
          drag
            ? "border-indigo-500 bg-indigo-500/10"
            : "border-slate-700 hover:border-slate-500 bg-slate-900/30"
        )}
      >
        <UploadCloud className="mx-auto mb-2 text-slate-400" />
        <p className="text-sm text-slate-300">{label}</p>
        <p className="text-xs text-slate-500 mt-1">
          Drag & drop or click to browse
        </p>
        <input
          ref={inputRef}
          type="file"
          accept=".pdf,.txt,.md"
          multiple={multiple}
          className="hidden"
          onChange={(e) => handleFiles(e.target.files)}
        />
      </div>

      {files.length > 0 && (
        <ul className="mt-3 space-y-2">
          {files.map((f, i) => (
            <li
              key={`${f.name}-${i}`}
              className="flex items-center justify-between rounded-md border border-slate-800 bg-slate-900/40 px-3 py-2 text-sm"
            >
              <span className="flex items-center gap-2 text-slate-300 truncate">
                <FileText size={14} />
                {f.name}
              </span>
              <button
                onClick={() =>
                  onChange(files.filter((_, idx) => idx !== i))
                }
                className="text-slate-500 hover:text-rose-400"
              >
                <X size={14} />
              </button>
            </li>
          ))}
        </ul>
      )}
    </div>
  );
}
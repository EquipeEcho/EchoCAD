import { FileKind } from "../types/documents";

// Renderiza o simbolo principal da marca.
export function EchoCadIcon() {
  return (
    <svg viewBox="0 0 48 48" focusable="false" aria-hidden="true">
      <path
        d="M24 8.5 35.5 15v18L24 39.5 12.5 33V15Z"
        fill="none"
        stroke="currentColor"
        strokeLinejoin="round"
        strokeWidth="2.5"
      />
    </svg>
  );
}

// Renderiza o icone de modo escuro.
export function MoonIcon() {
  return (
    <svg viewBox="0 0 24 24" focusable="false" aria-hidden="true">
      <path
        d="M18.5 14.2A7.5 7.5 0 0 1 9.8 5.5a7.75 7.75 0 1 0 8.7 8.7Z"
        fill="none"
        stroke="currentColor"
        strokeLinecap="round"
        strokeLinejoin="round"
        strokeWidth="1.8"
      />
    </svg>
  );
}

// Renderiza o icone de modo claro.
export function SunIcon() {
  return (
    <svg viewBox="0 0 24 24" focusable="false" aria-hidden="true">
      <circle cx="12" cy="12" r="4" fill="none" stroke="currentColor" strokeWidth="1.8" />
      <path
        d="M12 2.75v2.5m0 13.5v2.5m6.54-15.79-1.77 1.77M7.23 16.77l-1.77 1.77m13.29-6.54h2.5m-18 0h2.5m12.79 4.77 1.77 1.77M7.23 7.23 5.46 5.46"
        fill="none"
        stroke="currentColor"
        strokeLinecap="round"
        strokeWidth="1.8"
      />
    </svg>
  );
}

// Renderiza o icone de upload.
export function UploadIcon() {
  return (
    <svg viewBox="0 0 24 24" focusable="false" aria-hidden="true">
      <path
        d="M12 15V5m0 0-4 4m4-4 4 4M5 16.5V18a2 2 0 0 0 2 2h10a2 2 0 0 0 2-2v-1.5"
        fill="none"
        stroke="currentColor"
        strokeLinecap="round"
        strokeLinejoin="round"
        strokeWidth="1.8"
      />
    </svg>
  );
}

// Renderiza o ícone de visualização.
export function EyeIcon() {
  return (
    <svg viewBox="0 0 24 24" focusable="false" aria-hidden="true">
      <path
        d="M2.5 12s3.5-5.5 9.5-5.5 9.5 5.5 9.5 5.5-3.5 5.5-9.5 5.5S2.5 12 2.5 12Z"
        fill="none"
        stroke="currentColor"
        strokeLinejoin="round"
        strokeWidth="1.8"
      />
      <circle cx="12" cy="12" r="2.6" fill="none" stroke="currentColor" strokeWidth="1.8" />
    </svg>
  );
}

export function EyeOffIcon() {
  return (
    <svg viewBox="0 0 24 24" focusable="false" aria-hidden="true">
      <path
        d="M3.5 4.5 20.5 19.5"
        fill="none"
        stroke="currentColor"
        strokeLinecap="round"
        strokeWidth="1.8"
      />
      <path
        d="M9.2 6.9A9.9 9.9 0 0 1 12 6.5c6 0 9.5 5.5 9.5 5.5a15.2 15.2 0 0 1-2.8 3.2M6.1 8.7A15.1 15.1 0 0 0 2.5 12s3.5 5.5 9.5 5.5a9.7 9.7 0 0 0 4-.8"
        fill="none"
        stroke="currentColor"
        strokeLinecap="round"
        strokeLinejoin="round"
        strokeWidth="1.8"
      />
      <path
        d="M10.4 10.6a2.6 2.6 0 0 0 3 3"
        fill="none"
        stroke="currentColor"
        strokeLinecap="round"
        strokeWidth="1.8"
      />
    </svg>
  );
}

// Renderiza o ícone de remoção.
export function TrashIcon() {
  return (
    <svg viewBox="0 0 24 24" focusable="false" aria-hidden="true">
      <path
        d="M9.5 3.75h5m-8 3h11m-9.5 0v10a1.75 1.75 0 0 0 1.75 1.75h4.5A1.75 1.75 0 0 0 16 16.75v-10m-4.75 3v4.75m3.5-4.75v4.75"
        fill="none"
        stroke="currentColor"
        strokeLinecap="round"
        strokeLinejoin="round"
        strokeWidth="1.8"
      />
    </svg>
  );
}

// Renderiza o icone de download.
export function DownloadIcon() {
  return (
    <svg viewBox="0 0 24 24" focusable="false" aria-hidden="true">
      <path
        d="M12 4.5V14m0 0-3.5-3.5M12 14l3.5-3.5M5 16.5V18a2 2 0 0 0 2 2h10a2 2 0 0 0 2-2v-1.5"
        fill="none"
        stroke="currentColor"
        strokeLinecap="round"
        strokeLinejoin="round"
        strokeWidth="1.8"
      />
    </svg>
  );
}

// Renderiza o icone de avancar.
export function ChevronPlayIcon() {
  return (
    <svg viewBox="0 0 18 18" focusable="false" aria-hidden="true">
      <path d="M4 3.5 14 9 4 14.5Z" fill="currentColor" />
    </svg>
  );
}

// Renderiza o icone de sucesso.
export function CheckCircleIcon() {
  return (
    <svg viewBox="0 0 24 24" focusable="false" aria-hidden="true">
      <circle cx="12" cy="12" r="9" fill="none" stroke="currentColor" strokeWidth="1.8" />
      <path
        d="m8.5 12 2.3 2.4 4.7-5.2"
        fill="none"
        stroke="currentColor"
        strokeLinecap="round"
        strokeLinejoin="round"
        strokeWidth="1.8"
      />
    </svg>
  );
}

// Renderiza o icone do toast de sucesso.
export function ToastSuccessIcon() {
  return (
    <svg viewBox="0 0 24 24" focusable="false" aria-hidden="true">
      <circle cx="12" cy="12" r="10" fill="currentColor" />
      <path
        d="m8.6 12.2 2.1 2.2 4.8-5.4"
        fill="none"
        stroke="#ffffff"
        strokeLinecap="round"
        strokeLinejoin="round"
        strokeWidth="2"
      />
    </svg>
  );
}

// Renderiza o ícone de informação.
export function InfoCircleIcon() {
  return (
    <svg viewBox="0 0 24 24" focusable="false" aria-hidden="true">
      <circle cx="12" cy="12" r="9" fill="none" stroke="currentColor" strokeWidth="1.8" />
      <path
        d="M12 10.2v5.1m0-8.3h.01"
        fill="none"
        stroke="currentColor"
        strokeLinecap="round"
        strokeWidth="1.8"
      />
    </svg>
  );
}

// Renderiza o icone de fechar.
export function CloseIcon() {
  return (
    <svg viewBox="0 0 24 24" focusable="false" aria-hidden="true">
      <path
        d="m6 6 12 12M18 6 6 18"
        fill="none"
        stroke="currentColor"
        strokeLinecap="round"
        strokeWidth="1.8"
      />
    </svg>
  );
}

// Renderiza o icone de expandir.
export function ChevronDownIcon() {
  return (
    <svg viewBox="0 0 24 24" focusable="false" aria-hidden="true">
      <path
        d="m6 9 6 6 6-6"
        fill="none"
        stroke="currentColor"
        strokeLinecap="round"
        strokeLinejoin="round"
        strokeWidth="1.8"
      />
    </svg>
  );
}

// Renderiza o icone de recolher.
export function ChevronUpIcon() {
  return (
    <svg viewBox="0 0 24 24" focusable="false" aria-hidden="true">
      <path
        d="m18 15-6-6-6 6"
        fill="none"
        stroke="currentColor"
        strokeLinecap="round"
        strokeLinejoin="round"
        strokeWidth="1.8"
      />
    </svg>
  );
}

// Renderiza o icone de carregamento.
export function SpinnerIcon({ className }: { className?: string }) {
  return (
    <svg className={className} viewBox="0 0 24 24" focusable="false" aria-hidden="true">
      <path
        d="M12 3.25a8.75 8.75 0 1 1-6.19 2.56"
        fill="none"
        stroke="currentColor"
        strokeLinecap="round"
        strokeWidth="1.8"
      />
    </svg>
  );
}

export function UserIcon() {
  return (
    <svg viewBox="0 0 24 24" focusable="false" aria-hidden="true">
      <circle cx="12" cy="8" r="3.25" fill="none" stroke="currentColor" strokeWidth="1.8" />
      <path
        d="M5.5 19.5a6.5 6.5 0 0 1 13 0"
        fill="none"
        stroke="currentColor"
        strokeLinecap="round"
        strokeWidth="1.8"
      />
    </svg>
  );
}

export function LockIcon() {
  return (
    <svg viewBox="0 0 24 24" focusable="false" aria-hidden="true">
      <path
        d="M7 10V8a5 5 0 0 1 10 0v2"
        fill="none"
        stroke="currentColor"
        strokeLinecap="round"
        strokeWidth="1.8"
      />
      <rect
        x="5.5"
        y="10"
        width="13"
        height="10"
        rx="2"
        fill="none"
        stroke="currentColor"
        strokeWidth="1.8"
      />
    </svg>
  );
}

export function LogOutIcon() {
  return (
    <svg viewBox="0 0 24 24" focusable="false" aria-hidden="true">
      <path
        d="M9.5 5.5H7A2 2 0 0 0 5 7.5v9A2 2 0 0 0 7 18.5h2.5M14 8l4 4-4 4m3.5-4h-9"
        fill="none"
        stroke="currentColor"
        strokeLinecap="round"
        strokeLinejoin="round"
        strokeWidth="1.8"
      />
    </svg>
  );
}

// Escolhe o icone conforme o tipo do arquivo.
export function FileTypeIcon({ kind }: { kind: FileKind }) {
  if (kind === "project") {
    return (
      <svg viewBox="0 0 24 24" focusable="false" aria-hidden="true">
        <path
          d="M6.5 5.5h11v13h-11v-13Z"
          fill="none"
          stroke="currentColor"
          strokeLinejoin="round"
          strokeWidth="1.8"
        />
        <path
          d="M9 9h6M9 12h6M9 15h3.5"
          fill="none"
          stroke="currentColor"
          strokeLinecap="round"
          strokeLinejoin="round"
          strokeWidth="1.8"
        />
      </svg>
    );
  }

  if (kind === "pdf") {
    return (
      <svg viewBox="0 0 24 24" focusable="false" aria-hidden="true">
        <path
          d="M8 3.5h6l4.5 4.5v11A1.5 1.5 0 0 1 17 20.5H8A1.5 1.5 0 0 1 6.5 19V5A1.5 1.5 0 0 1 8 3.5Z"
          fill="none"
          stroke="currentColor"
          strokeLinejoin="round"
          strokeWidth="1.8"
        />
        <path
          d="M14 3.5V8h4.5M9 11.5h5M9 15h6M9 18.5h6"
          fill="none"
          stroke="currentColor"
          strokeLinecap="round"
          strokeLinejoin="round"
          strokeWidth="1.8"
        />
      </svg>
    );
  }

  return (
    <svg viewBox="0 0 24 24" focusable="false" aria-hidden="true">
      <path
        d="M8 3.5h6l4.5 4.5v11A1.5 1.5 0 0 1 17 20.5H8A1.5 1.5 0 0 1 6.5 19V5A1.5 1.5 0 0 1 8 3.5Z"
        fill="none"
        stroke="currentColor"
        strokeLinejoin="round"
        strokeWidth="1.8"
      />
      <path
        d="M14 3.5V8h4.5"
        fill="none"
        stroke="currentColor"
        strokeLinejoin="round"
        strokeWidth="1.8"
      />
    </svg>
  );
}

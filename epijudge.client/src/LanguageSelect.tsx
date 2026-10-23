import { LANGUAGES } from './workspaceModels';

export function LanguageSelect({
  value,
  onChange,
  label,
  disabled = false,
}: {
  value: string;
  onChange: (language: string) => void;
  label: string;
  disabled?: boolean;
}) {
  return (
    <div className="language-selector-wrapper">
      <select
        className="language-select"
        value={value}
        onChange={(event) => onChange(event.target.value)}
        disabled={disabled}
        aria-label={label}
      >
        {LANGUAGES.map((language) => (
          <option key={language.id} value={language.id}>
            {language.label}
          </option>
        ))}
      </select>
    </div>
  );
}

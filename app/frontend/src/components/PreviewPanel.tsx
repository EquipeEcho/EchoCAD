import { GeneratedDocument } from "../types/documents";
import { formatInputDate } from "../utils/date";

type PreviewPanelProps = {
  document: GeneratedDocument;
};

// Exibe a pré-visualização do documento gerado.
export function PreviewPanel({ document }: PreviewPanelProps) {
  const projectDate = document.projectInfo?.projectDate
    ? formatInputDate(document.projectInfo.projectDate)
    : document.createdAt;
  const documentFacts = [
    { label: "Projeto", value: document.projectInfo?.name || document.title },
    { label: "Referência", value: document.reference },
    { label: "Data do projeto", value: projectDate },
    { label: "Arquivos-base", value: `${document.sourceFiles.length} itens` },
  ];

  if (document.projectInfo?.responsible) {
    documentFacts.push({
      label: "Responsável",
      value: document.projectInfo.responsible,
    });
  }

  return (
    <section className="preview-panel surface-card" aria-labelledby="preview-title">
      <div className="preview-panel__header">
        <div>
          <p className="preview-panel__eyebrow">
            Pré-visualização do memorial de cálculo
          </p>
          <h2 className="preview-panel__title" id="preview-title">
            {document.title}
          </h2>
        </div>
        <span className="preview-panel__badge">{document.versionLabel}</span>
      </div>

      <div className="preview-paper">
        <div className="preview-paper__intro">
          <p className="preview-paper__kicker">MEMORIAL DESCRITIVO E DE CÁLCULO</p>
          <h3 className="preview-paper__heading">{document.subtitle}</h3>
          <p className="preview-paper__summary">{document.summary}</p>
        </div>

        <div className="preview-paper__facts">
          {documentFacts.map((fact) => (
            <div className="preview-paper__fact" key={fact.label}>
              <span className="preview-paper__fact-label">{fact.label}</span>
              <strong className="preview-paper__fact-value">{fact.value}</strong>
            </div>
          ))}
        </div>

        <div className="preview-paper__content">
          <div className="preview-paper__section">
            <h4 className="preview-paper__section-title">Síntese técnica</h4>
            {document.previewLines.map((line) => (
              <p key={line} className="preview-paper__line">
                {line}
              </p>
            ))}
          </div>

          <aside className="preview-paper__aside" aria-label="Dados complementares">
            <div className="preview-paper__panel">
              <h4 className="preview-paper__panel-title">Arquivos de origem</h4>
              <ul className="preview-paper__source-list">
                {document.sourceFiles.map((fileName) => (
                  <li className="preview-paper__source-item" key={fileName}>
                    {fileName}
                  </li>
                ))}
              </ul>
            </div>

            {document.projectInfo?.notes ? (
              <div className="preview-paper__panel">
                <h4 className="preview-paper__panel-title">Observações</h4>
                <p className="preview-paper__note">{document.projectInfo.notes}</p>
              </div>
            ) : null}

            <div className="preview-table">
              <div className="preview-table__header">
                <span>Parâmetro</span>
                <span>Valor</span>
              </div>
              {document.tableRows.map((row) => (
                <div className="preview-table__row" key={row.label}>
                  <span>{row.label}</span>
                  <strong>{row.value}</strong>
                </div>
              ))}
            </div>
          </aside>
        </div>

        <div className="preview-paper__footer-note">
          Documento gerado em ambiente de protótipo para validação visual do fluxo
          EchoCAD.
        </div>
      </div>
    </section>
  );
}

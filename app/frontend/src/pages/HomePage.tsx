import { SectionTitle } from "../components/SectionTitle";
import { UploadPanel } from "../components/UploadPanel";

// Exibe a tela inicial com a área de upload.
export function HomePage() {
  return (
    <main className="page page--home">
      <div className="page__content home-layout">
        <section className="home-intro" aria-labelledby="home-heading">
          <div className="home-intro__copy">
            <SectionTitle
              eyebrow="EchoCAD"
              titleId="home-heading"
              title="Análise de dados CAD"
              description="Plataforma para automatização de documentos técnicos. Envie seus projetos para gerar memoriais de cálculo e especificações técnicas de forma clara, rápida e organizada."
            />
          </div>
        </section>

        <div className="home-divider" aria-hidden="true" />

        <UploadPanel />
      </div>
    </main>
  );
}

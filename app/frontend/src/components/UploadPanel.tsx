import { ChangeEvent, DragEvent, MouseEvent, useRef, useState } from "react";
import { useNavigate } from "react-router-dom";
import { usePrototype } from "../providers/PrototypeProvider";
import {
  ProjectSaveInput,
  UploadDocument,
  UploadStatusTone,
} from "../types/documents";
import { Button } from "./Button";
import { ConfirmationModal } from "./ConfirmationModal";
import { FileList } from "./FileList";
import { FileRow } from "./FileRow";
import {
  ChevronPlayIcon,
  EyeIcon,
  InfoCircleIcon,
  TrashIcon,
  UploadIcon,
} from "./Icons";
import { ProjectSaveModal } from "./ProjectSaveModal";
import { PlantaCADModal, PlantaCADInfo } from "./PlantaCADModal";
import { createProjeto, createMultiplePlantasCAD } from "../services/api";

// Monta a mensagem de status após selecionar arquivos.
function buildUploadStatusMessage(
  addedCount: number,
  duplicateCount: number,
  invalidCount: number,
  totalCount: number,
) {
  if (addedCount > 0) {
    return {
      message:
        totalCount === 1
          ? "Arquivo selecionado"
          : `${totalCount} arquivos selecionados`,
      tone: "success" as UploadStatusTone,
    };
  }

  if (invalidCount > 0) {
    return {
      message: "Somente arquivos PDF, DWG e DXF são aceitos.",
      tone: "error" as UploadStatusTone,
    };
  }

  if (duplicateCount > 0) {
    return {
      message: "Os arquivos selecionados já estavam na lista.",
      tone: "info" as UploadStatusTone,
    };
  }

  return {
    message: "Formatos aceitos: PDF, DWG e DXF.",
    tone: "info" as UploadStatusTone,
  };
}

function getSuggestedProjectName(files: UploadDocument[]) {
  const primaryFileName = files[0]?.name.replace(/\.[^.]+$/, "");

  if (!primaryFileName) {
    return "";
  }

  return primaryFileName.replace(/[_-]+/g, " ").trim();
}

// Controla a seleção e o envio dos arquivos do frontend.
export function UploadPanel() {
  const navigate = useNavigate();
  const inputRef = useRef<HTMLInputElement>(null);
  const [isDragging, setIsDragging] = useState(false);
  const [statusMessage, setStatusMessage] = useState(
    "Formatos aceitos: PDF, DWG e DXF.",
  );
  const [statusTone, setStatusTone] = useState<UploadStatusTone>("info");
  const [filePendingRemoval, setFilePendingRemoval] =
    useState<UploadDocument | null>(null);
  const [showProjectSaveModal, setShowProjectSaveModal] = useState(false);
  const [showPlantaCADModal, setShowPlantaCADModal] = useState(false);
  const [isSavingProject, setIsSavingProject] = useState(false);
  const [currentPlantaInfo, setCurrentPlantaInfo] = useState<PlantaCADInfo | null>(null);
  const {
    uploadedFiles,
    addUploadedFiles,
    removeUploadedFile,
    simulatePreviewAction,
    showToast,
  } = usePrototype();

  // Processa os arquivos escolhidos e atualiza o status.
  const applyFileSelection = (files: FileList | File[]) => {
    const result = addUploadedFiles(files);
    const nextTotalCount = uploadedFiles.length + result.addedCount;
    const nextStatus = buildUploadStatusMessage(
      result.addedCount,
      result.duplicateCount,
      result.invalidCount,
      nextTotalCount,
    );

    setStatusMessage(nextStatus.message);
    setStatusTone(nextStatus.tone);

    if (result.addedCount > 0) {
      showToast(
        result.addedCount === 1
          ? "Arquivo adicionado com sucesso."
          : `${result.addedCount} arquivos adicionados com sucesso.`,
        "success",
      );
      // Mostrar modal de planta CAD quando novos arquivos são adicionados
      setShowPlantaCADModal(true);
    } else if (result.invalidCount > 0) {
      showToast(nextStatus.message, "error");
    }
  };

  // Abre o seletor nativo de arquivos.
  const openFilePicker = () => {
    if (!inputRef.current) {
      return;
    }

    inputRef.current.value = "";
    inputRef.current.click();
  };

  // Evita que o clique do botão dispare também o clique da área de upload.
  const handleFilePickerButtonClick = (
    event: MouseEvent<HTMLButtonElement>,
  ) => {
    event.stopPropagation();
    openFilePicker();
  };

  // Trata arquivos escolhidos pelo input.
  const handleInputChange = (event: ChangeEvent<HTMLInputElement>) => {
    if (!event.target.files) {
      return;
    }

    applyFileSelection(event.target.files);
  };

  // Trata arquivos soltos na área de upload.
  const handleDrop = (event: DragEvent<HTMLDivElement>) => {
    event.preventDefault();
    setIsDragging(false);
    applyFileSelection(event.dataTransfer.files);
  };

  // Remove o arquivo após confirmação do usuário.
  const handleRemoveConfirm = () => {
    if (!filePendingRemoval) {
      return;
    }

    removeUploadedFile(filePendingRemoval.id);
    showToast("Arquivo removido da lista.", "info");
    setFilePendingRemoval(null);
  };

  const handleStartProcessingClick = () => {
    if (uploadedFiles.length === 0) {
      showToast("Nenhum arquivo selecionado.", "error");
      return;
    }

    setShowProjectSaveModal(true);
  };

  // Captura informações de planta CAD quando arquivos são adicionados
  const handlePlantaCADSave = (plantaInfo: PlantaCADInfo) => {
    setCurrentPlantaInfo(plantaInfo);
    setShowPlantaCADModal(false);
  };

  // Envia os arquivos, planta CAD e informações do projeto para o processamento
  const handleProjectSave = async (projectInfo: ProjectSaveInput) => {
    if (uploadedFiles.length === 0) {
      showToast("Nenhum arquivo selecionado.", "error");
      setShowProjectSaveModal(false);
      return;
    }

    if (!currentPlantaInfo) {
      showToast("Informações da planta CAD não encontradas.", "error");
      return;
    }

    setIsSavingProject(true);
    setShowProjectSaveModal(false);

    try {
      // Criar projeto
      // Nota: Usando id_usuario = 1 como padrão. Em um app real, obtenha do sistema de autenticação
      const createdProject = await createProjeto({
        name: projectInfo.name,
        description: projectInfo.descricao,
        client: projectInfo.cliente,
        id_user: 1, // TODO: Obter ID real do usuário do sistema de autenticação
      });

      showToast("Projeto criado com sucesso!", "success");

      // Criar entradas de planta CAD para cada arquivo enviado
      const plantasData = uploadedFiles.map((file) => ({
        tipo: currentPlantaInfo.tipo,
        arquivo: currentPlantaInfo.arquivo || file.name,
      }));

      await createMultiplePlantasCAD(plantasData, createdProject.id);

      showToast("Plantas CAD criadas com sucesso!", "success");

      // Navegar para página de processamento com informações do projeto
      navigate("/processando", {
        state: {
          files: uploadedFiles,
          projectInfo,
          projectId: createdProject.id,
        },
      });
    } catch (error) {
      console.error("Erro ao salvar projeto:", error);
      showToast(
        error instanceof Error ? error.message : "Erro ao salvar projeto",
        "error"
      );
      setIsSavingProject(false);
      // Reabrir modal para que o usuário tente novamente
      setShowProjectSaveModal(true);
    }
  };

  return (
    <section className="upload-column" aria-labelledby="upload-title">
      <div className="section-heading">
        <p className="section-heading__eyebrow" id="upload-title">
          ÁREA DE UPLOAD
        </p>
      </div>

      <input
        ref={inputRef}
        className="upload-panel__input"
        type="file"
        accept=".dwg,.dxf,.pdf"
        multiple
        onChange={handleInputChange}
      />

      {uploadedFiles.length === 0 ? (
        <div
          className={`upload-empty${isDragging ? " is-dragging" : ""}`}
          onClick={openFilePicker}
          onDragOver={(event) => {
            event.preventDefault();
            setIsDragging(true);
          }}
          onDragLeave={() => setIsDragging(false)}
          onDrop={handleDrop}
          role="button"
          tabIndex={0}
          onKeyDown={(event) => {
            if (event.key === "Enter" || event.key === " ") {
              event.preventDefault();
              openFilePicker();
            }
          }}
        >
          <div className="upload-empty__icon" aria-hidden="true">
            <UploadIcon />
          </div>
          <p className="upload-empty__title">Envie seus arquivos técnicos</p>
          <p className="upload-empty__description">
            Arraste documentos CAD ou clique para selecionar arquivos do
            computador.
          </p>
          <Button
            variant="primary"
            size="lg"
            onClick={handleFilePickerButtonClick}
          >
            Selecionar arquivos
          </Button>
        </div>
      ) : (
        <>
          <FileList
            header={
              <div className="file-list-card__header-row">
                <p className="file-list-card__title">
                  {uploadedFiles.length} arquivos selecionados
                </p>
                <button
                  className="text-action"
                  type="button"
                  onClick={openFilePicker}
                >
                  + Adicionar mais
                </button>
              </div>
            }
          >
            <div className="stack">
              {uploadedFiles.map((document) => (
                <FileRow
                  key={document.id}
                  name={document.name}
                  kind={document.kind}
                  actions={[
                    {
                      label: `Visualizar ${document.name}`,
                      icon: <EyeIcon />,
                      onClick: () => simulatePreviewAction(document.name),
                    },
                    {
                      label: `Remover ${document.name}`,
                      icon: <TrashIcon />,
                      onClick: () => setFilePendingRemoval(document),
                      tone: "danger",
                    },
                  ]}
                />
              ))}
            </div>
          </FileList>

          <div className="upload-actions">
            <p
              aria-live="polite"
              className={`status-note status-note--${statusTone}`}
              role="status"
            >
              <span className="status-note__icon" aria-hidden="true">
                <InfoCircleIcon />
              </span>
              <span>{statusMessage}</span>
            </p>

            <div className="upload-actions__buttons">
              <Button variant="primary" onClick={openFilePicker}>
                Adicionar arquivos
              </Button>
              <Button
                variant="success"
                trailingIcon={<ChevronPlayIcon />}
                onClick={handleStartProcessingClick}
              >
                Salvar projeto
              </Button>
            </div>
          </div>
        </>
      )}

      <ConfirmationModal
        open={Boolean(filePendingRemoval)}
        title="Remover arquivo"
        description={
          <p>
            Deseja remover <strong>{filePendingRemoval?.name}</strong> da lista
            de upload?
          </p>
        }
        confirmLabel="Remover"
        onClose={() => setFilePendingRemoval(null)}
        onConfirm={handleRemoveConfirm}
      />

      <ProjectSaveModal
        open={showProjectSaveModal}
        initialProjectName={getSuggestedProjectName(uploadedFiles)}
        subtitle="Preencha os dados do projeto que será salvo no sistema."
        cancelLabel="Cancelar"
        onClose={() => setShowProjectSaveModal(false)}
        onSave={handleProjectSave}
      />

      <PlantaCADModal
        open={showPlantaCADModal}
        onClose={() => {
          if (!isSavingProject) {
            setShowPlantaCADModal(false);
          }
        }}
        onSave={handlePlantaCADSave}
      />
    </section>
  );
}

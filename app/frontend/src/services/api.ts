// API base URL - configure this based on your environment
const API_BASE_URL = import.meta.env.VITE_API_URL || "http://localhost:8000";

interface ProjetoCreatePayload {
  nome: string;
  descricao?: string;
  cliente?: string;
  id_usuario: number;
}

interface PlantaCADCreatePayload {
  tipo?: string;
  arquivo?: string;
  ids_projeto: number[];
}
  
interface ProjectResponse {
  id: number;
  nome: string;
  descricao?: string;
  cliente?: string;
  data_criacao: string;
  id_usuario: number;
}

interface PlantaCADResponse {
  id: number;
  tipo?: string;
  arquivo?: string;
  ids_projeto: number[];
}

/**
 * Creates a new project in the database
 * @param projectData Project information to create
 * @returns The created project with its ID
 */
export async function createProjeto(
  projectData: ProjetoCreatePayload
): Promise<ProjectResponse> {
  const response = await fetch(`${API_BASE_URL}/projeto/`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify(projectData),
  });

  if (!response.ok) {
    const error = await response.json();
    throw new Error(error.detail || "Erro ao criar projeto");
  }

  return response.json();
}

/**
 * Creates a new planta CAD for a project
 * @param plantaData Plant CAD information to create
 * @returns The created planta CAD with its ID
 */
export async function createPlantaCAD(
  plantaData: PlantaCADCreatePayload
): Promise<PlantaCADResponse> {
  const response = await fetch(`${API_BASE_URL}/planta_cad/`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify(plantaData),
  });

  if (!response.ok) {
    const error = await response.json();
    throw new Error(error.detail || "Erro ao criar planta CAD");
  }

  return response.json();
}

/**
 * Creates multiple plantas CAD for a project
 * @param plantasData Array of plant CAD information to create
 * @param projectId The project ID
 * @returns Array of created plantas CAD
 */
export async function createMultiplePlantasCAD(
  plantasData: Omit<PlantaCADCreatePayload, "ids_projeto">[],
  projectId: number
): Promise<PlantaCADResponse[]> {
  const results: PlantaCADResponse[] = [];

  for (const plantaData of plantasData) {
    const result = await createPlantaCAD({
      ...plantaData,
      ids_projeto: [projectId],
    });
    results.push(result);
  }

  return results;
}

/**
 * Fetches a project by ID
 * @param projectId The project ID
 * @returns The project data
 */
export async function getProjeto(projectId: number): Promise<ProjectResponse> {
  const response = await fetch(`${API_BASE_URL}/projeto/${projectId}`);

  if (!response.ok) {
    throw new Error("Erro ao buscar projeto");
  }

  return response.json();
}

/**
 * Lists all projects
 * @returns Array of all projects
 */
export async function listProjetos(): Promise<ProjectResponse[]> {
  const response = await fetch(`${API_BASE_URL}/projeto/`);

  if (!response.ok) {
    throw new Error("Erro ao listar projetos");
  }

  return response.json();
}

// Criar norma (upsert já acontece no backend)
export async function createNorma(data: {
  nome: string;
  conexao?: string;
  status?: boolean;
  ids_projeto: number[];
}) {
  const response = await fetch(`${API_BASE_URL}/norma/`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify(data),
  });

  if (!response.ok) {
    const error = await response.json();
    throw new Error(error.detail || "Erro ao criar norma");
  }

  return response.json();
}

// Listar normas
export async function listNormas() {
  const response = await fetch(`${API_BASE_URL}/norma/`);

  if (!response.ok) {
    throw new Error("Erro ao buscar normas");
  }

  return response.json();
}
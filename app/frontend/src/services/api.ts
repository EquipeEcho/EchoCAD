// API base URL - configure this based on your environment
const API_BASE_URL = import.meta.env.VITE_API_URL || "http://localhost:8000";

export interface AuthUser {
  id: number;
  name: string;
  email: string;
  role?: string | null;
  created_at?: string;
  message?: string;
}

export interface RegisterPayload {
  name: string;
  email: string;
  password: string;
  role?: string;
}

export interface LoginPayload {
  email: string;
  password: string;
}

export interface AuthResponse {
  user: AuthUser;
}

interface ProjetoCreatePayload {
  name: string;
  description?: string;
  client?: string;
  id_user: number;
}

interface PlantaCADCreatePayload {
  discipline?: string;
  path?: string;
  id_project: number;
}
  
interface ProjectResponse {
  id: number;
  name: string;
  description?: string;
  client?: string;
  created_at: string;
  id_user: number;
}

interface PlantaCADResponse {
  id: number;
  discipline?: string;
  path?: string;
  id_project: number;
}

interface NormaCreatePayload {
  nome: string;
  //status?: string;
  ids_projeto: number[]; // Verifique se no Python está "ids_projeto" ou "projeto_id"
}

async function parseErrorMessage(response: Response, fallbackMessage: string) {
  try {
    const errorData = await response.json();
    if (typeof errorData.detail === "string") {
      return errorData.detail;
    }

    return errorData.detail?.[0]?.msg || fallbackMessage;
  } catch {
    return fallbackMessage;
  }
}

export async function registerUser(userData: RegisterPayload): Promise<AuthResponse> {
  const response = await fetch(`${API_BASE_URL}/users/`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify(userData),
  });

  if (!response.ok) {
    throw new Error(await parseErrorMessage(response, "Erro ao cadastrar usuário"));
  }

  return { user: await response.json() };
}

export async function loginUser(credentials: LoginPayload): Promise<AuthResponse> {
  const response = await fetch(`${API_BASE_URL}/users/login`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify(credentials),
  });

  if (!response.ok) {
    throw new Error(await parseErrorMessage(response, "Erro ao fazer login"));
  }

  return { user: await response.json() };
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
 * Uploads a file for a specific project
 * @param projectId The project ID
 * @param file The file to upload
 * @returns Upload response with the saved path
 */
export async function uploadFile(
  projectId: number,
  file: File
): Promise<{ message: string; filename: string; path: string }> {
  const formData = new FormData();
  formData.append("file", file);

  const response = await fetch(`${API_BASE_URL}/upload/${projectId}`, {
    method: "POST",
    body: formData,
  });

  if (!response.ok) {
    const error = await response.json();
    throw new Error(error.detail || "Erro ao fazer upload do arquivo");
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
  plantasData: Omit<PlantaCADCreatePayload, "id_project">[],
  projectId: number
): Promise<PlantaCADResponse[]> {
  const results: PlantaCADResponse[] = [];

  for (const plantaData of plantasData) {
    const result = await createPlantaCAD({
      ...plantaData,
      id_project: projectId,
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

/**
 * Starts AI processing for a project
 * @param projectId The project ID
 * @param stream Whether to stream the response
 * @returns The processing results or a Response for streaming
 */
export async function processProject(projectId: number, stream: boolean = false) {
  const url = `${API_BASE_URL}/processamento/${projectId}${stream ? "?stream=true" : ""}`;
  
  if (stream) {
    return fetch(url, { method: "POST" });
  }

  const response = await fetch(url, {
    method: "POST",
  });

  if (!response.ok) {
    const error = await response.json();
    throw new Error(error.detail || "Erro ao processar projeto");
  }

  return response.json();
}

/**
 * Fetches the saved AI analysis results for a project
 * @param projectId The project ID
 */
export async function getProjectResult(projectId: number) {
  const response = await fetch(`${API_BASE_URL}/processamento/${projectId}/resultado`);
  
  if (!response.ok) {
    if (response.status === 404) return null;
    throw new Error("Erro ao buscar resultado do processamento");
  }

  return response.json();
}

// Criar norma (upsert já acontece no backend)
export async function createNorma(data: NormaCreatePayload) {
  const response = await fetch(`${API_BASE_URL}/norma/`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify(data),
  });

  if (!response.ok) {
    // Melhoria: Capturar o erro detalhado do FastAPI (422)
    const errorData = await response.json();
    console.error("Erro detalhado do servidor:", errorData);
    throw new Error(errorData.detail?.[0]?.msg || "Erro ao criar norma");
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

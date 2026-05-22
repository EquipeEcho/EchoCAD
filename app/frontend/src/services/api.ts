// API base URL - configure this based on your environment
export const API_BASE_URL = import.meta.env.VITE_API_URL || "/api";

export interface AuthUser {
  id: number;
  name: string;
  email: string;
  role?: string | null;
  created_at?: string;
  message?: string;
}

export interface AuthSession {
  access_token: string;
  token_type: string;
  user: AuthUser;
}

export interface AuthResponse extends AuthSession {}

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

interface ProjetoCreatePayload {
  name: string;
  description?: string;
  client?: string;
  id_user: number;
}

const AUTH_SESSION_KEY = "echocad_auth_user";

function getStoredAuthSession(): AuthSession | null {
  const stored = window.localStorage.getItem(AUTH_SESSION_KEY);
  if (!stored) {
    return null;
  }

  try {
    const parsed = JSON.parse(stored);
    if (parsed && typeof parsed === "object" && "access_token" in parsed && "user" in parsed) {
      return parsed as AuthSession;
    }
  } catch {
    window.localStorage.removeItem(AUTH_SESSION_KEY);
  }

  return null;
}

export function getAuthHeaders(): HeadersInit | undefined {
  const session = getStoredAuthSession();
  if (!session?.access_token) {
    console.warn("No auth token found in session");
    return undefined;
  }

  console.log("Using auth token:", session.access_token.substring(0, 20) + "...");
  return {
    Authorization: `Bearer ${session.access_token}`,
  };
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

  return await response.json();
}

export async function loginUser(credentials: LoginPayload): Promise<AuthResponse> {
  console.log("Sending login request to:", `${API_BASE_URL}/users/login`);
  
  const response = await fetch(`${API_BASE_URL}/users/login`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify(credentials),
  });

  if (!response.ok) {
    const errorMsg = await parseErrorMessage(response, "Erro ao fazer login");
    console.error("Login failed:", response.status, errorMsg);
    throw new Error(errorMsg);
  }

  const data = await response.json();
  console.log("Login response:", { 
    has_access_token: !!data.access_token, 
    token_type: data.token_type,
    has_user: !!data.user,
    user_id: data.user?.id 
  });
  
  return data;
}

/**
 * Creates a new project in the database
 * @param projectData Project information to create
 * @returns The created project with its ID
 */
export async function createProjeto(
  projectData: ProjetoCreatePayload
): Promise<ProjectResponse> {
  const response = await fetch(`${API_BASE_URL}/project/`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      ...(getAuthHeaders() ?? {}),
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
    headers: {
      ...(getAuthHeaders() ?? {}),
    },
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
      ...(getAuthHeaders() ?? {}),
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
  const response = await fetch(`${API_BASE_URL}/project/?projeto_id=${projectId}`, {
    headers: {
      ...(getAuthHeaders() ?? {}),
    },
  });

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
  const headers = getAuthHeaders() ?? {};
  console.log("Fetching projects with headers:", Object.keys(headers));
  
  const response = await fetch(`${API_BASE_URL}/project/all`, {
    headers,
  });
  console.log("Fetching project list with status:", response.status);

  if (!response.ok) {
    const errorData = await response.json().catch(() => ({}));
    console.error("Failed to list projects:", response.status, errorData);
    throw new Error("Erro ao listar projetos");
  }

  const data = await response.json();
  console.log("Projects fetched:", data.length);
  return data;
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
    return fetch(url, { method: "POST", headers: { ...(getAuthHeaders() ?? {}) } });
  }

  const response = await fetch(url, {
    method: "POST",
    headers: {
      ...(getAuthHeaders() ?? {}),
    },
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
  const response = await fetch(`${API_BASE_URL}/processamento/${projectId}/resultado`, {
    headers: {
      ...(getAuthHeaders() ?? {}),
    },
  });
  
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
      ...(getAuthHeaders() ?? {}),
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
  const response = await fetch(`${API_BASE_URL}/norma/`, {
    headers: {
      ...(getAuthHeaders() ?? {}),
    },
  });

  if (!response.ok) {
    throw new Error("Erro ao buscar normas");
  }

  return response.json();
}

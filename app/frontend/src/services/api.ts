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

export interface ChangePasswordPayload {
  current_password: string;
  new_password: string;
}

export interface GroqApiKeyStatus {
  configured: boolean;
  masked_key?: string | null;
  message: string;
}

interface ProjetoCreatePayload {
  name: string;
  description?: string;
  client?: string;
  id_user: number;
}

export const AUTH_SESSION_KEY = "echocad_auth_user";
export const SESSION_EXPIRED_EVENT = "echocad:session-expired";
export const SESSION_EXPIRED_MESSAGE =
  "Sua sessão expirou. Faça login novamente.";

type JwtPayload = {
  exp?: number;
};

function canUseBrowserStorage() {
  return typeof window !== "undefined" && Boolean(window.localStorage);
}

function decodeJwtPayload(token: string): JwtPayload | null {
  const payload = token.split(".")[1];

  if (!payload) {
    return null;
  }

  try {
    const normalizedPayload = payload.replace(/-/g, "+").replace(/_/g, "/");
    const paddedPayload = normalizedPayload.padEnd(
      Math.ceil(normalizedPayload.length / 4) * 4,
      "=",
    );

    return JSON.parse(window.atob(paddedPayload)) as JwtPayload;
  } catch {
    return null;
  }
}

export function getSessionExpirationTime(session: AuthSession | null) {
  if (!session?.access_token) {
    return null;
  }

  const payload = decodeJwtPayload(session.access_token);

  return payload?.exp ? payload.exp * 1000 : null;
}

export function isAuthSessionExpired(session: AuthSession | null) {
  const expiresAt = getSessionExpirationTime(session);

  return Boolean(expiresAt && expiresAt <= Date.now());
}

export function clearStoredAuthSession() {
  if (canUseBrowserStorage()) {
    window.localStorage.removeItem(AUTH_SESSION_KEY);
  }
}

export function notifySessionExpired(message = SESSION_EXPIRED_MESSAGE) {
  if (typeof window === "undefined") {
    return;
  }

  window.dispatchEvent(
    new CustomEvent(SESSION_EXPIRED_EVENT, {
      detail: { message },
    }),
  );
}

export function readStoredAuthSession(): AuthSession | null {
  if (!canUseBrowserStorage()) {
    return null;
  }

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

function getStoredAuthSession(): AuthSession | null {
  const session = readStoredAuthSession();

  if (isAuthSessionExpired(session)) {
    clearStoredAuthSession();
    notifySessionExpired();
    return null;
  }

  return session;
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

export async function changePassword(
  payload: ChangePasswordPayload,
): Promise<AuthUser> {
  const response = await fetch(`${API_BASE_URL}/users/me/password`, {
    method: "PATCH",
    headers: {
      "Content-Type": "application/json",
      ...(getAuthHeaders() ?? {}),
    },
    body: JSON.stringify(payload),
  });

  if (!response.ok) {
    await throwAuthenticatedApiError(response, "Erro ao alterar senha");
  }

  return response.json();
}

export async function getGroqApiKeyStatus(): Promise<GroqApiKeyStatus> {
  const response = await fetch(`${API_BASE_URL}/users/me/groq-key`, {
    headers: {
      ...(getAuthHeaders() ?? {}),
    },
  });

  if (!response.ok) {
    await throwAuthenticatedApiError(response, "Erro ao buscar chave Groq");
  }

  return response.json();
}

export async function saveGroqApiKey(apiKey: string): Promise<GroqApiKeyStatus> {
  const response = await fetch(`${API_BASE_URL}/users/me/groq-key`, {
    method: "PUT",
    headers: {
      "Content-Type": "application/json",
      ...(getAuthHeaders() ?? {}),
    },
    body: JSON.stringify({ api_key: apiKey }),
  });

  if (!response.ok) {
    await throwAuthenticatedApiError(response, "Erro ao salvar chave Groq");
  }

  return response.json();
}

export async function removeGroqApiKey(): Promise<GroqApiKeyStatus> {
  const response = await fetch(`${API_BASE_URL}/users/me/groq-key`, {
    method: "DELETE",
    headers: {
      ...(getAuthHeaders() ?? {}),
    },
  });

  if (!response.ok) {
    await throwAuthenticatedApiError(response, "Erro ao remover chave Groq");
  }

  return response.json();
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
    await throwAuthenticatedApiError(response, "Erro ao criar projeto");
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
    await throwAuthenticatedApiError(response, "Erro ao fazer upload do arquivo");
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
    await throwAuthenticatedApiError(response, "Erro ao criar planta CAD");
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
    await throwAuthenticatedApiError(response, "Erro ao buscar projeto");
  }

  return response.json();
}

export async function deleteProjeto(projectId: number): Promise<void> {
  const response = await fetch(
    `${API_BASE_URL}/project/?projeto_id=${projectId}`,
    {
      method: "DELETE",
      headers: {
        ...(getAuthHeaders() ?? {}),
      },
    },
  );

  if (!response.ok) {
    await throwAuthenticatedApiError(response, "Erro ao remover projeto");
  }
}

async function throwAuthenticatedApiError(response: Response, fallbackMessage: string) {
  if (response.status === 401) {
    clearStoredAuthSession();
    notifySessionExpired();
    throw new Error(SESSION_EXPIRED_MESSAGE);
  }

  throw new Error(await parseErrorMessage(response, fallbackMessage));
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
    console.error("Failed to list projects:", response.status);
    await throwAuthenticatedApiError(response, "Erro ao listar projetos");
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
    const response = await fetch(url, {
      method: "POST",
      headers: { ...(getAuthHeaders() ?? {}) },
    });

    if (!response.ok) {
      await throwAuthenticatedApiError(response, "Erro ao processar projeto");
    }

    return response;
  }

  const response = await fetch(url, {
    method: "POST",
    headers: {
      ...(getAuthHeaders() ?? {}),
    },
  });

  if (!response.ok) {
    await throwAuthenticatedApiError(response, "Erro ao processar projeto");
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
    await throwAuthenticatedApiError(response, "Erro ao buscar resultado do processamento");
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
    await throwAuthenticatedApiError(response, "Erro ao criar norma");
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
    await throwAuthenticatedApiError(response, "Erro ao buscar normas");
  }

  return response.json();
}

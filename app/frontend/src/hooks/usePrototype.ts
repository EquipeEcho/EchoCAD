import { useContext } from "react";
import { PrototypeContext } from "../providers/PrototypeProvider";

// Retorna o contexto principal do protótipo.
export function usePrototype() {
  const context = useContext(PrototypeContext);

  if (!context) {
    throw new Error("usePrototype must be used within PrototypeProvider.");
  }

  return context;
}

"use client";

import React, { createContext, useContext, useReducer, useCallback, useEffect } from "react";
import type { RequirementPriority, RequirementStatus } from "@/types";
import { businessRequirements as defaultReqs } from "@/data/content/requirements-data";

const STORAGE_KEY = "ba-compass-requirements-edits";

export interface EditableRequirement {
  id: string;
  statement: string;
  priority: RequirementPriority;
  status: RequirementStatus;
  stakeholderOwner: string;
  justification: string;
  relatedKpi: string;
  _edited: boolean;
  _original: string;
}

interface RequirementsState {
  requirements: EditableRequirement[];
  editMode: boolean;
}

type RequirementsAction =
  | { type: "ENTER_EDIT_MODE" }
  | { type: "EXIT_EDIT_MODE" }
  | { type: "UPDATE_REQUIREMENT"; id: string; field: string; value: string }
  | { type: "RESET_REQUIREMENT"; id: string }
  | { type: "RESET_ALL" }
  | { type: "LOAD_EDITS"; edits: Record<string, Record<string, string>> };

function buildDefaultRequirements(): EditableRequirement[] {
  return defaultReqs.map((r) => ({
    id: r.id,
    statement: r.statement,
    priority: r.priority as RequirementPriority,
    status: r.status as RequirementStatus,
    stakeholderOwner: r.stakeholderOwner,
    justification: r.justification,
    relatedKpi: r.relatedKpi,
    _edited: false,
    _original: r.statement,
  }));
}

function reducer(state: RequirementsState, action: RequirementsAction): RequirementsState {
  switch (action.type) {
    case "ENTER_EDIT_MODE":
      return { ...state, editMode: true };
    case "EXIT_EDIT_MODE":
      return { ...state, editMode: false };
    case "UPDATE_REQUIREMENT": {
      const reqs = state.requirements.map((r) => {
        if (r.id !== action.id) return r;
        const updated = { ...r, [action.field]: action.value, _edited: true };
        return updated;
      });
      return { ...state, requirements: reqs };
    }
    case "RESET_REQUIREMENT": {
      const reqs = state.requirements.map((r) => {
        if (r.id !== action.id) return r;
        const original = defaultReqs.find((d) => d.id === r.id);
        return {
          id: r.id,
          statement: original?.statement || r.statement,
          priority: (original?.priority || r.priority) as RequirementPriority,
          status: (original?.status || r.status) as RequirementStatus,
          stakeholderOwner: original?.stakeholderOwner || r.stakeholderOwner,
          justification: original?.justification || r.justification,
          relatedKpi: original?.relatedKpi || r.relatedKpi,
          _edited: false,
          _original: original?.statement || r.statement,
        };
      });
      return { ...state, requirements: reqs };
    }
    case "RESET_ALL":
      return { requirements: buildDefaultRequirements(), editMode: false };
    case "LOAD_EDITS": {
      const reqs = state.requirements.map((r) => {
        const edit = action.edits[r.id];
        if (!edit) return r;
        return { ...r, ...edit, _edited: true };
      });
      return { ...state, requirements: reqs };
    }
    default:
      return state;
  }
}

interface RequirementsContextValue {
  state: RequirementsState;
  enterEditMode: () => void;
  exitEditMode: () => void;
  updateRequirement: (id: string, field: string, value: string) => void;
  resetRequirement: (id: string) => void;
  resetAll: () => void;
  getEditedCount: () => number;
}

const RequirementsContext = createContext<RequirementsContextValue | null>(null);

export function RequirementsProvider({ children }: { children: React.ReactNode }) {
  const [state, dispatch] = useReducer(reducer, { requirements: buildDefaultRequirements(), editMode: false });

  // Load edits from localStorage on mount
  useEffect(() => {
    try {
      const stored = localStorage.getItem(STORAGE_KEY);
      if (stored) {
        const edits = JSON.parse(stored);
        dispatch({ type: "LOAD_EDITS", edits });
      }
    } catch {
      // localStorage unavailable or corrupt — use defaults
    }
  }, []);

  // Save edits to localStorage whenever requirements change
  useEffect(() => {
    try {
      const edits: Record<string, Record<string, string>> = {};
      for (const r of state.requirements) {
        if (r._edited) {
          edits[r.id] = {
            statement: r.statement,
            priority: r.priority,
            status: r.status,
            stakeholderOwner: r.stakeholderOwner,
            justification: r.justification,
            relatedKpi: r.relatedKpi,
          };
        }
      }
      localStorage.setItem(STORAGE_KEY, JSON.stringify(edits));
    } catch {
      // storage full or disabled — silently continue
    }
  }, [state.requirements]);

  const enterEditMode = useCallback(() => dispatch({ type: "ENTER_EDIT_MODE" }), []);
  const exitEditMode = useCallback(() => dispatch({ type: "EXIT_EDIT_MODE" }), []);
  const updateRequirement = useCallback((id: string, field: string, value: string) => dispatch({ type: "UPDATE_REQUIREMENT", id, field, value }), []);
  const resetRequirement = useCallback((id: string) => dispatch({ type: "RESET_REQUIREMENT", id }), []);
  const resetAll = useCallback(() => {
    localStorage.removeItem(STORAGE_KEY);
    dispatch({ type: "RESET_ALL" });
  }, []);
  const getEditedCount = useCallback(() => state.requirements.filter((r) => r._edited).length, [state.requirements]);

  return (
    <RequirementsContext.Provider value={{ state, enterEditMode, exitEditMode, updateRequirement, resetRequirement, resetAll, getEditedCount }}>
      {children}
    </RequirementsContext.Provider>
  );
}

export function useRequirements() {
  const ctx = useContext(RequirementsContext);
  if (!ctx) throw new Error("useRequirements must be used within RequirementsProvider");
  return ctx;
}

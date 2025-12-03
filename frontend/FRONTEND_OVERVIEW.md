# Frontend Overview

This document describes the structure, runtime flow, and important files for the frontend of DigitalDemo. It includes a Mermaid diagram showing the main runtime interactions between UI, API client, and the backend.

**Location:** `frontend/`

---

## Quick Summary

- Framework: React + TypeScript (Vite)
- Main entry: `src/main.tsx`
- Router: `src/App.tsx`
- Centralized API config: `src/config/api.ts`
- API client (single source of truth): `src/services/apiClient.ts`

---

## File Map (important files)

- `src/main.tsx` — Application bootstrap
- `src/App.tsx` — Route definitions
- `src/config/api.ts` — Centralized API endpoint config (reads `VITE_API_BASE_URL`)
- `src/services/apiClient.ts` — Singleton API client and exported TypeScript types

Screens:
- `src/screens/DocumentList.tsx` — `/documents`
- `src/screens/UploadScreen.tsx` — `/upload`
- `src/screens/DocumentDetails.tsx` — `/documents/:docId`
- `src/screens/ResultPage.tsx` — debug JSON view

Components:
- `src/components/Layout.tsx` — layout and navigation
- `src/components/PDFViewer.tsx` — PDF viewing component (react-pdf-viewer)

Other:
- `public/` — static assets
- `.env.local`, `.env.production`, `.env.example` — environment variables

---

## High-level Data Flow

- The UI calls the `apiClient` for all network operations. The client constructs URLs from `src/config/api.ts` which reads `VITE_API_BASE_URL` from env.
- Uploads go to `POST /api/upload`. Backend saves file and creates DB record.
- External worker processes documents and calls backend notify endpoints to set `processing` / `ready` and attach result paths.
- Frontend lists documents with `GET /api/documents`. When a document is `ready`, the details page fetches JSON result and loads the PDF URL.

---

## Mermaid Diagram (runtime flow)

```mermaid
flowchart LR
  subgraph UI
    U[User]
    Upload[UploadScreen]\n(`/upload`)
    List[DocumentList]\n(`/documents`)
    Details[DocumentDetails]\n(`/documents/:docId`)
  end

  subgraph Frontend
    APIConfig[`src/config/api.ts`]
    APIClient[`src/services/apiClient.ts`]
    PDFViewer[`src/components/PDFViewer.tsx`]
  end

  subgraph Backend
    BackendAPI[FastAPI Backend]\n`/api/*`
    Storage[Storage (incoming/results)]
    DB[SQLite DB]
    Worker[External Processor]
  end

  U -->|visit| List
  U -->|visit| Upload
  List -->|click "View"| Details
  Upload -->|submit file| APIClient
  Details -->|loads| PDFViewer

  APIClient -->|POST /api/upload| BackendAPI
  BackendAPI -->|save file| Storage
  BackendAPI -->|insert row status=queued| DB

  Worker -->|processes file & writes results| Storage
  Worker -->|POST /api/notify/result-ready| BackendAPI
  BackendAPI -->|update result paths + status=ready| DB

  Details -->|GET /api/results/json/:docId| BackendAPI
  PDFViewer -->|GET pdf url (/api/results/pdf/:docId)| BackendAPI

  List -->|GET /api/documents| BackendAPI

  style UI fill:#f9f,stroke:#333,stroke-width:1px
  style Frontend fill:#fffbcc,stroke:#333,stroke-width:1px
  style Backend fill:#ccf2ff,stroke:#333,stroke-width:1px
```

---

## How components use the API client (examples)

- `DocumentList.tsx` calls `apiClient.listDocuments()` and renders the table.
- `UploadScreen.tsx` calls `apiClient.uploadDocument(file, type)`.
- `DocumentDetails.tsx` calls `apiClient.getProcessedDocument(docId)` and `apiClient.getPDFUrl(docId)` for the viewer.

These calls hide URL construction and error handling inside `apiClient`.

---

## Run / Dev commands (PowerShell)

Start backend (dev):

```powershell
cd c:\DigitalDemo\backend
C:/Python314/python.exe -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8808
```

Start frontend (dev):

```powershell
cd c:\DigitalDemo\frontend
npm install
npm run dev
# Vite will report the URL (e.g. http://localhost:5173 or next free port)
```

---

## Notes & Suggestions

- Use `import type { ... }` when importing TypeScript-only types in `.tsx` files (we fixed the module import error earlier).
- Consider adding a small polling hook (or React Query) to refresh document statuses automatically while processing is ongoing.
- Keep `apiClient` as the single place to add auth headers, retry logic, or request logging.

---

If you'd like, I can:
- Generate a PNG of the Mermaid diagram (or an SVG) and add it to `public/`.
- Add a small `hooks/useDocumentStatus.ts` that polls a document's status until `ready`.
- Expand this doc with a component call graph or sequence diagrams.

Which of these would you like next?

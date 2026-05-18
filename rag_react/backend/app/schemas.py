from pydantic import BaseModel, Field, field_validator
from typing import List, Optional, Dict, Any

class FiltrosRequest(BaseModel):
    nodos: List[str] = Field(default=[], description="Lista de nodos territoriales seleccionados")
    formalizacion: List[str] = Field(default=[], description="Estados de formalización")
    rango_edad: List[str] = Field(default=[], description="Rangos de edad")
    nivel_educativo: List[str] = Field(default=[], description="Niveles educativos")
    estrato: List[str] = Field(default=[], description="Estratos socioeconómicos")
    antiguedad_negocio: List[str] = Field(default=[], description="Antigüedad del negocio")
    tipo_vivienda: List[str] = Field(default=[], description="Tipo de vivienda")

    @field_validator('nodos', 'formalizacion', 'rango_edad', 'nivel_educativo', 'estrato', 'antiguedad_negocio', 'tipo_vivienda')
    @classmethod
    def sanitize_strings(cls, v: List[str]) -> List[str]:
        # Prevenir cualquier intento de inyección básica limpiando caracteres no permitidos en los filtros
        sanitized = []
        for item in v:
            clean_item = "".join(c for c in item if c.isalnum() or c in " .,-_/áéíóúÁÉÍÓÚñÑüÜ")
            sanitized.append(clean_item)
        return sanitized

class ConsultaRagRequest(BaseModel):
    consigna: str = Field(..., min_length=2, max_length=1000, description="Pregunta o instrucción para el agente RAG")
    filtros: FiltrosRequest = Field(default_factory=FiltrosRequest)
    
    @field_validator('consigna')
    @classmethod
    def sanitize_consigna(cls, v: str) -> str:
        if ".." in v or "/bin/" in v or "cgi-bin" in v:
            raise ValueError("Consigna contiene patrones no permitidos.")
        return v

class BivariadoRequest(BaseModel):
    dim1: str = Field(..., description="Primera dimensión psicométrica")
    dim2: str = Field(..., description="Segunda dimensión psicométrica")
    filtros: FiltrosRequest = Field(default_factory=FiltrosRequest)


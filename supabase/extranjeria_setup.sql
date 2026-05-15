-- ========================================================
-- LEXLY SAAS - Extranjería Database Setup
-- Ejecute este SQL en el Supabase SQL Editor
-- ========================================================

-- ========================================================
-- 1. MODIFICAR TABLA CASOS - Agregar campos de extranjería
-- ========================================================

-- Agregar campos si no existen
ALTER TABLE casos ADD COLUMN IF NOT EXISTS tipo_procedimiento TEXT;
ALTER TABLE casos ADD COLUMN IF NOT EXISTS estado_extranjeria TEXT DEFAULT 'inicial';
ALTER TABLE casos ADD COLUMN IF NOT EXISTS fecha_presentacion DATE;
ALTER TABLE casos ADD COLUMN IF NOT EXISTS fecha_resolucion DATE;
ALTER TABLE casos ADD COLUMN IF NOT EXISTS numero_expediente_oficial TEXT;
ALTER TABLE casos ADD COLUMN IF NOT EXISTS resultado TEXT;
ALTER TABLE casos ADD COLUMN IF NOT EXISTS observaciones_internas TEXT;

-- Actualizar comentarios de columnas
COMMENT ON COLUMN casos.tipo_procedimiento IS 'Tipo de procedimiento: arraigo_social, arraigo_laboral, arraigo_familiar, arraigo_formacion, arraigo_2_oportunidad, reagrupacion_familiar, residencia_trabajo, nacionalidad, otro';
COMMENT ON COLUMN casos.estado_extranjeria IS 'Estado del procedimiento: inicial, documentacion, presentado, plazo, resuelto, denegado, archivado';
COMMENT ON COLUMN casos.numero_expediente_oficial IS 'Número de expediente en la Oficina de Extranjería';

-- ========================================================
-- 2. CREAR TABLA: caso_documentos
-- Documentos requeridos para cada caso
-- ========================================================

CREATE TABLE IF NOT EXISTS caso_documentos (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    caso_id UUID NOT NULL REFERENCES casos(id) ON DELETE CASCADE,
    
    -- Clasificación del documento
    categoria TEXT NOT NULL,  -- 'identidad', 'residencia', 'laborales', 'economicos', 'penales', 'integracion', 'otro'
    nombre TEXT NOT NULL,       -- Descripción específica del documento
    
    -- Estado del documento
    estado TEXT DEFAULT 'pendiente',  -- 'pendiente', 'requerido', 'entregado', 'rechazado', 'no_aplica'
    
    -- Fechas de seguimiento
    fecha_requerido DATE,
    fecha_entregado DATE,
    fecha_vencimiento DATE,
    
    -- Detalles
    notas TEXT,
    archivo_url TEXT,
    
    -- Timestamps
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Índices para mejor rendimiento
CREATE INDEX IF NOT EXISTS idx_caso_documentos_caso ON caso_documentos(caso_id);
CREATE INDEX IF NOT EXISTS idx_caso_documentos_estado ON caso_documentos(estado);
CREATE INDEX IF NOT EXISTS idx_caso_documentos_categoria ON caso_documentos(categoria);

-- ========================================================
-- 3. CREAR TABLA: caso_actividades
-- Timeline de actividades del caso (citas, llamadas, etc.)
-- ========================================================

CREATE TABLE IF NOT EXISTS caso_actividades (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    caso_id UUID NOT NULL REFERENCES casos(id) ON DELETE CASCADE,
    
    -- Tipo de actividad
    tipo TEXT NOT NULL,  -- 'cita', 'llamada', 'email', 'reunion', 'presentacion', 'notificacion', 'requerimiento', 'gestion', 'otro'
    titulo TEXT NOT NULL,
    descripcion TEXT,
    
    -- Resultado
    resultado TEXT,
    resultado_detalle TEXT,
    
    -- Fechas
    fecha_actividad DATE NOT NULL,
    proxima_accion TEXT,
    fecha_proxima_accion DATE,
    
    -- Estado de seguimiento
    estado TEXT DEFAULT 'pendiente',  -- 'pendiente', 'completado', 'en_progreso'
    
    -- Timestamps
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    created_by UUID REFERENCES auth.users(id)
);

-- Índices
CREATE INDEX IF NOT EXISTS idx_caso_actividades_caso ON caso_actividades(caso_id);
CREATE INDEX IF NOT EXISTS idx_caso_actividades_fecha ON caso_actividades(fecha_actividad);
CREATE INDEX IF NOT EXISTS idx_caso_actividades_tipo ON caso_actividades(tipo);

-- ========================================================
-- 4. CREAR TABLA: caso_notas
-- Notas internas del abogado
-- ========================================================

CREATE TABLE IF NOT EXISTS caso_notas (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    caso_id UUID NOT NULL REFERENCES casos(id) ON DELETE CASCADE,
    
    -- Contenido
    contenido TEXT NOT NULL,
    
    -- Tipo de nota
    tipo TEXT DEFAULT 'interna',  -- 'interna', 'atencion', 'soporte', 'revisor', 'urgente'
    
    -- Visibilidad
    privada BOOLEAN DEFAULT TRUE,  -- True = solo visible para abogados
    
    -- Timestamps
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    created_by UUID REFERENCES auth.users(id),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Índices
CREATE INDEX IF NOT EXISTS idx_caso_notas_caso ON caso_notas(caso_id);
CREATE INDEX IF NOT EXISTS idx_caso_notas_tipo ON caso_notas(tipo);

-- ========================================================
-- 5. CREAR TABLA: plantillas_documentos
-- Plantillas de documentos requeridos por tipo de procedimiento
-- ========================================================

CREATE TABLE IF NOT EXISTS plantillas_documentos (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    
    --关联
    tipo_procedimiento TEXT NOT NULL,
    
    -- Documento
    nombre TEXT NOT NULL,
    categoria TEXT NOT NULL,
    descripcion TEXT,
    
    -- Requisitos
    obligatorio BOOLEAN DEFAULT TRUE,
    observaciones TEXT,
    
    -- Orden en checklist
    orden INTEGER DEFAULT 0,
    
    -- Estado
    activa BOOLEAN DEFAULT TRUE,
    
    -- Timestamps
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Insertar plantillas por defecto para cada tipo de arraigo
-- ARRAIGO SOCIAL
INSERT INTO plantillas_documentos (tipo_procedimiento, nombre, categoria, descripcion, orden) VALUES
('arraigo_social', 'Pasaporte vigente', 'identidad', 'Pasaporte del país de origen con validez mínima', 1),
('arraigo_social', 'Certificado de nacimiento', 'identidad', 'Apostillado y traducido', 2),
('arraigo_social', 'Certificado de matrimonio', 'identidad', 'Si procede, apostillado', 3),
('arraigo_social', 'Certificado de antecedentes penales', 'penales', 'Del país de origen, apostillado', 4),
('arraigo_social', 'Certificado de antecedentes UE', 'penales', 'Del país donde haya residido los últimos 5 años', 5),
('arraigo_social', 'Registro de empadronamiento', 'residencia', '3 años continuados', 6),
('arraigo_social', 'Informe de integración social', 'integracion', 'Emitido por la Comunidad Autónoma', 7),
('arraigo_social', 'Contrato de trabajo', 'laborales', 'O demostración de medios económicos', 8),
('arraigo_social', 'Documentación médica', 'salud', 'Seguro médico o SS', 9),
('arraigo_social', 'Fotos tipo carné', 'identidad', '2 fotos recientes', 10);

-- ARRAIGO LABORAL
INSERT INTO plantillas_documentos (tipo_procedimiento, nombre, categoria, descripcion, orden) VALUES
('arraigo_laboral', 'Pasaporte vigente', 'identidad', 'Pasaporte del país de origen', 1),
('arraigo_laboral', 'Certificado de nacimiento', 'identidad', 'Apostillado y traducido', 2),
('arraigo_laboral', 'Certificado de antecedentes penales', 'penales', 'Del país de origen', 3),
('arraigo_laboral', 'Documentación laboral', 'laborales', 'Sentencia judicial o acta de Inspección de Trabajo', 4),
('arraigo_laboral', 'Nómina o recibos', 'laborales', 'últimos 6 meses', 5),
('arraigo_laboral', 'Contrato de trabajo', 'laborales', 'Si ya tienes', 6),
('arraigo_laboral', 'Registro de empadronamiento', 'residencia', '2 años continuados', 7);

-- ARRAIGO FAMILIAR
INSERT INTO plantillas_documentos (tipo_procedimiento, nombre, categoria, descripcion, orden) VALUES
('arraigo_familiar', 'Pasaporte vigente', 'identidad', 'Pasaporte del familiar', 1),
('arraigo_familiar', 'DNI español', 'identidad', 'Del familiar español', 2),
('arraigo_familiar', 'Certificado de nacimiento hijo/a', 'identidad', 'Del menor español', 3),
('arraigo_familiar', 'Certificado de matrimonio', 'identidad', 'Si es cónyuge', 4),
('arraigo_familiar', 'Libro de familia', 'identidad', 'Si procede', 5),
('arraigo_familiar', 'Certificado de residencia', 'residencia', 'Del familiar español', 6),
('arraigo_familiar', 'Certificado de antecedentes penales', 'penales', 'Del solicitante', 7);

-- REAGRUPACIÓN FAMILIAR
INSERT INTO plantillas_documentos (tipo_procedimiento, nombre, categoria, descripcion, orden) VALUES
('reagrupacion', 'Pasaporte del reagrupante', 'identidad', 'Vigente', 1),
('reagrupacion', 'DNI/TIE reagrupante', 'identidad', 'Temporal o largo duración', 2),
('reagrupacion', 'Certificado de nacimiento familiar', 'identidad', 'Apostillado', 3),
('reagrupacion', 'Certificado de matrimonio', 'identidad', 'Si es cónyuge, apostillado', 4),
('reagrupacion', 'Libro de familia', 'identidad', 'Si procede', 5),
('reagrupacion', 'Certificado de resize', 'residencia', 'Mínimo 1 año', 6),
('reagrupacion', 'Ingresos mínimos', 'economicos', '400% IPREM', 7),
('reagrupacion', 'Informe de vivienda', 'residencia', 'Adecuada según normativa', 8),
('reagrupacion', 'Seguro médico', 'salud', 'Público o privado', 9);

-- ========================================================
-- 6. AGREGAR ENABLE ROW SECURITY PARA TODAS LAS TABLAS
-- ========================================================

ALTER TABLE caso_documentos ENABLE ROW LEVEL SECURITY;
ALTER TABLE caso_actividades ENABLE ROW LEVEL SECURITY;
ALTER TABLE caso_notas ENABLE ROW LEVEL SECURITY;
ALTER TABLE plantillas_documentos ENABLE ROW LEVEL SECURITY;

-- ========================================================
-- 7. POLÍTICAS BÁSICAS (ajuste según su necesidad)
-- ========================================================

-- Permiten acceso total a usuarios autenticados (ajustar para producción)
DROP POLICY IF EXISTS "Allow all on caso_documentos" ON caso_documentos;
CREATE POLICY "Allow all on caso_documentos" ON caso_documentos FOR ALL USING (true);

DROP POLICY IF EXISTS "Allow all on caso_actividades" ON caso_actividades;
CREATE POLICY "Allow all on caso_actividades" ON caso_actividades FOR ALL USING (true);

DROP POLICY IF EXISTS "Allow all on caso_notas" ON caso_notas;
CREATE POLICY "Allow all on caso_notas" ON caso_notas FOR ALL USING (true);

DROP POLICY IF EXISTS "Allow all on plantillas_documentos" ON plantillas_documentos;
CREATE POLICY "Allow all on plantillas_documentos" ON plantillas_documentos FOR ALL USING (true);

-- ========================================================
-- VERIFICACIÓN
-- ========================================================

SELECT 'Tablas creadas correctamente' as resultado;

-- Verificar tablas
SELECT table_name 
FROM information_schema.tables 
WHERE table_schema = 'public' 
AND table_name IN ('caso_documentos', 'caso_actividades', 'caso_notas', 'plantillas_documentos');

-- Verificar columnas añadidas a casos
SELECT column_name, data_type 
FROM information_schema.columns 
WHERE table_name = 'casos' 
AND column_name IN ('tipo_procedimiento', 'estado_extranjeria', 'fecha_presentacion', 'fecha_resolucion', 'numero_expediente_oficial');
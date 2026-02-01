-- Add priority column to notes
ALTER TABLE notes
ADD COLUMN IF NOT EXISTS priority VARCHAR(20) NOT NULL DEFAULT 'medium';

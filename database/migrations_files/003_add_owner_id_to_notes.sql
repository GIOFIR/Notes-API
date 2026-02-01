-- -- Add owner_id to notes
-- ALTER TABLE notes
-- ADD COLUMN IF NOT EXISTS owner_id INTEGER;

-- -- add constraint on notes accordance to owner id
-- ALTER TABLE notes
-- ADD CONSTRAINT IF NOT EXISTS fk_notes_owner
-- FOREIGN KEY (owner_id) REFERENCES users(id) ON DELETE CASCADE;

-- -- Index for faster lookups by owner_id
-- CREATE INDEX IF NOT EXISTS idx_notes_owner_id ON notes(owner_id);


-- 1) Add column (Postgres supports IF NOT EXISTS here)
ALTER TABLE notes
ADD COLUMN IF NOT EXISTS owner_id INTEGER;

-- 2) Add FK constraint safely (Postgres DOES NOT support IF NOT EXISTS for constraints)
DO $$
BEGIN
    IF NOT EXISTS (
        SELECT 1
        FROM pg_constraint
        WHERE conname = 'fk_notes_owner'
    ) THEN
        ALTER TABLE notes
        ADD CONSTRAINT fk_notes_owner
        FOREIGN KEY (owner_id) REFERENCES users(id) ON DELETE CASCADE;
    END IF;
END $$;

-- 3) Add index safely
CREATE INDEX IF NOT EXISTS idx_notes_owner_id ON notes(owner_id);

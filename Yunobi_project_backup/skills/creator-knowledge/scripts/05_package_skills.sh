#!/usr/bin/env bash
# Step 5: Package each skill directory into a .skill file (ZIP)
#
# Usage: bash scripts/05_package_skills.sh
# Output: .skill files in project root

set -e

SKILLS_DIR="skills"
OUTPUT_DIR="packaged"

mkdir -p "$OUTPUT_DIR"

echo "Packaging skills..."

for skill_dir in "$SKILLS_DIR"/kallaway-*/; do
    if [ ! -d "$skill_dir" ]; then
        continue
    fi
    
    skill_name=$(basename "$skill_dir")
    
    # Validate SKILL.md exists
    if [ ! -f "$skill_dir/SKILL.md" ]; then
        echo "  SKIP: $skill_name (no SKILL.md found)"
        continue
    fi
    
    # Check line count
    lines=$(wc -l < "$skill_dir/SKILL.md")
    if [ "$lines" -gt 500 ]; then
        echo "  WARNING: $skill_name SKILL.md has $lines lines (limit: 500)"
    fi
    
    # Package as .skill (ZIP)
    output_file="$OUTPUT_DIR/${skill_name}.skill"
    (cd "$SKILLS_DIR" && zip -r "../$output_file" "$skill_name/")
    
    echo "  ✓ $output_file ($lines lines)"
done

echo ""
echo "Done! Packaged skills in $OUTPUT_DIR/"
echo ""
echo "To install a skill in Claude Code:"
echo "  claude skill install packaged/kallaway-hooks.skill"
echo ""
echo "To install all:"
echo "  for f in packaged/*.skill; do claude skill install \"\$f\"; done"

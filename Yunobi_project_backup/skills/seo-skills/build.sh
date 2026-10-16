#!/bin/bash
# Build script for seo-skills
# Creates individual skill zips and complete bundle in dist/

set -e

VERSION="1.0.0"
DIST_DIR="dist"

echo "Building seo-skills v${VERSION}..."
echo "================================="

# Create dist directory
mkdir -p "$DIST_DIR"

# Remove existing zips
rm -f "$DIST_DIR"/*.zip

# Individual skill packages (for Claude.ai upload)
SKILLS=(
  "seo-on-page-optimization"
  "seo-technical-audit"
  "seo-content-strategy"
  "seo-schema-structured-data"
  "seo-off-page-backlinks"
  "seo-local-seo"
  "seo-mcp-tools-expert"
)

for skill in "${SKILLS[@]}"; do
  echo "Packaging ${skill}..."
  (cd skills && zip -rq "../${DIST_DIR}/${skill}-v${VERSION}.zip" "${skill}" -x "*/.DS_Store")
done

# Complete bundle (for Claude Code plugin install)
echo "Packaging complete bundle..."
zip -rq "${DIST_DIR}/seo-mcp-skills-v${VERSION}.zip" \
  .claude-plugin/ \
  skills/ \
  CLAUDE.md \
  README.md \
  LICENSE \
  .mcp.json.example \
  -x "*/.DS_Store"

echo ""
echo "Build complete!"
echo "================================="
echo ""
echo "Individual skills:"
for skill in "${SKILLS[@]}"; do
  SIZE=$(du -h "${DIST_DIR}/${skill}-v${VERSION}.zip" | cut -f1)
  echo "  ${DIST_DIR}/${skill}-v${VERSION}.zip (${SIZE})"
done

echo ""
BUNDLE_SIZE=$(du -h "${DIST_DIR}/seo-mcp-skills-v${VERSION}.zip" | cut -f1)
echo "Complete bundle:"
echo "  ${DIST_DIR}/seo-mcp-skills-v${VERSION}.zip (${BUNDLE_SIZE})"

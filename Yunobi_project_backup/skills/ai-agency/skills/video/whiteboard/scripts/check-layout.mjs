#!/usr/bin/env node
/**
 * Layout gate for generated .excalidraw boards.
 *
 * Nothing else catches a caption sitting on a circle, because the file is valid
 * JSON either way and the board only looks wrong once it is on the iPad. Run it
 * on every build, before any push.
 *
 * Usage: node check-layout.mjs out/<board>.excalidraw [more.excalidraw ...]
 */

import { readFileSync } from 'node:fs'

const CENTRE_TOLERANCE = 8

const box = (el) => ({
	x1: el.x,
	y1: el.y,
	x2: el.x + el.width,
	y2: el.y + el.height,
	type: el.type,
	label: el.text ?? el.type,
})

const overlaps = (a, b) => a.x1 < b.x2 && b.x1 < a.x2 && a.y1 < b.y2 && b.y1 < a.y2
const centre = (a) => [(a.x1 + a.x2) / 2, (a.y1 + a.y2) / 2]

/** True when a shape is wrapped around the text rather than colliding with it. */
function concentric(a, b) {
	const [ax, ay] = centre(a)
	const [bx, by] = centre(b)
	return Math.abs(ax - bx) <= CENTRE_TOLERANCE && Math.abs(ay - by) <= CENTRE_TOLERANCE
}

/**
 * True when the text sits entirely inside the shape, which makes it that
 * shape's label rather than a collision.
 *
 * WHY: concentric only catches a single label centred on its shape. A brick
 * carrying a name and a caption has two labels, neither of them on the centre
 * line, and both are deliberate.
 */
function encloses(shape, t) {
	return shape.x1 <= t.x1 && shape.y1 <= t.y1 && shape.x2 >= t.x2 && shape.y2 >= t.y2
}

function check(path) {
	const scene = JSON.parse(readFileSync(path, 'utf8'))
	const els = scene.elements.map(box)
	const problems = []

	for (let i = 0; i < els.length; i += 1) {
		for (let j = i + 1; j < els.length; j += 1) {
			const [a, b] = [els[i], els[j]]
			if (!overlaps(a, b)) continue

			const types = [a.type, b.type].sort().join('/')
			// WHY: a label inside a node and a highlighter ring around a figure are
			// both concentric by construction, so only off-centre overlaps are real.
			if (types === 'ellipse/text' || types === 'rectangle/text') {
				const t = a.type === 'text' ? a : b
				const shape = a.type === 'text' ? b : a
				if (concentric(a, b) || encloses(shape, t)) continue
			}
			if (a.type !== 'text' && b.type !== 'text') continue
			if (types === 'arrow/text' || types === 'ellipse/ellipse') continue

			const text = a.type === 'text' ? a : b
			const other = a.type === 'text' ? b : a
			problems.push(`${types}  ${JSON.stringify(text.label)} over ${JSON.stringify(other.label)}`)
		}
	}

	const xs = scene.elements.flatMap((e) => [e.x, e.x + e.width])
	const ys = scene.elements.flatMap((e) => [e.y, e.y + e.height])
	const bounds = `x ${Math.min(...xs).toFixed(0)}..${Math.max(...xs).toFixed(0)}, y ${Math.min(...ys).toFixed(0)}..${Math.max(...ys).toFixed(0)}`

	console.log(`${path}  ${scene.elements.length} elements, ${bounds}`)
	for (const problem of problems) console.log(`  ${problem}`)
	return problems.length
}

const paths = process.argv.slice(2)
if (paths.length === 0) {
	console.error('Usage: node check-layout.mjs <board.excalidraw> [...]')
	process.exit(1)
}

const total = paths.reduce((sum, path) => sum + check(path), 0)
if (total > 0) {
	console.error(`\n${total} overlap${total === 1 ? '' : 's'}. Move the coordinates, rebuild, run again.`)
	process.exit(1)
}
console.log('\nlayout clean')

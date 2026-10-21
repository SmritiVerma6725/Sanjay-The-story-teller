/**
 * SignBridge — Milestone M3 Phase 3.1: Focused Data Contracts Test Suite
 *
 * Comprehensive unit tests for `SignBridgeContracts` (sign_contracts.js):
 * 1. Valid SignItem and SignSequence contracts and immutability (frozen objects).
 * 2. Missing required fields enforcement.
 * 3. Allowed enum values and consistency rules.
 * 4. Duration and media timestamp range boundaries.
 * 5. Nested child SignItem validation within SignSequence.
 * 6. Unsupported words validation and honest reporting telemetry.
 * 7. Fingerspelling category constraints (single A-Z character gloss).
 * 8. Optional decoupled animationId validation and regex rules.
 * 9. Integration check verifying all dependent modules load without missing dependency errors.
 *
 * Can be executed via: node extension/tests/test_sign_contracts.js
 */

'use strict';

const path = require('path');
const assert = require('assert');

// 1. Load SignBridgeContracts
const contractsPath = path.resolve(__dirname, '../models/sign_contracts.js');
const C = require(contractsPath);

let totalTests = 0;
let passedTests = 0;

function runTest(name, fn) {
  totalTests++;
  try {
    fn();
    passedTests++;
    console.log(`  ✔ PASS: ${name}`);
  } catch (err) {
    console.error(`  ✖ FAIL: ${name} -> ${err.message}`);
    throw err;
  }
}

console.log('===============================================================');
console.log(' SignBridge Milestone M3 — Focused Contract Unit Test Suite');
console.log('===============================================================');

// -----------------------------------------------------------------
// Suite 1: Valid Objects & Immutability Contracts
// -----------------------------------------------------------------
console.log('\n--- Suite 1: Valid Objects & Immutability Contracts ---');

runTest('Minimal valid SignItem', () => {
  const item = {
    gloss: 'HELLO',
    category: 'lexical',
    durationMs: 750,
    source: 'seed_dictionary'
  };
  const res = C.validateSignItem(item);
  assert.strictEqual(res.valid, true);
  assert.strictEqual(res.errors.length, 0);
});

runTest('Full valid SignItem with animationId and nonManualMarker', () => {
  const item = {
    gloss: 'THANK_YOU',
    category: 'lexical',
    durationMs: 900,
    source: 'seed_dictionary',
    animationId: 'anim_isl_thank_you_v1',
    nonManualMarker: {
      headTilt: 'forward',
      eyebrows: 'raised'
    }
  };
  const res = C.validateSignItem(item);
  assert.strictEqual(res.valid, true);
  assert.strictEqual(res.errors.length, 0);
});

runTest('Factory createSignItem produces frozen immutable object with defaults', () => {
  const item = C.createSignItem({
    gloss: 'welcome',
    durationMs: 800
  });
  assert.strictEqual(item.gloss, 'WELCOME', 'Gloss must be converted to uppercase');
  assert.strictEqual(item.category, 'lexical', 'Default category must be lexical');
  assert.strictEqual(item.source, 'seed_dictionary', 'Default source must be seed_dictionary');
  assert.strictEqual(item.animationId, null, 'Default animationId must be null');
  assert.strictEqual(Object.isFrozen(item), true, 'SignItem must be frozen');
});

runTest('Valid complete SignSequence with children and unsupported words', () => {
  const seq = {
    sequenceId: 'seq_chunk_001',
    language: 'ISL',
    rawTranscript: 'Hello world quantum',
    sourceChunkSeq: 1,
    startMediaTimeMs: 0,
    endMediaTimeMs: 2000,
    signs: [
      { gloss: 'HELLO', category: 'lexical', durationMs: 750, source: 'seed_dictionary' },
      { gloss: 'W', category: 'fingerspelling', durationMs: 300, source: 'fingerspell_fallback' }
    ],
    unsupportedWords: ['quantum'],
    fingerspellingApplied: true
  };
  const res = C.validateSignSequence(seq);
  assert.strictEqual(res.valid, true);
  assert.strictEqual(res.errors.length, 0);
});

runTest('Factory createSignSequence produces frozen immutable sequence and frozen arrays', () => {
  const seq = C.createSignSequence({
    sequenceId: 'seq_002',
    startMediaTimeMs: 2000,
    endMediaTimeMs: 4000,
    signs: [{ gloss: 'YES', category: 'lexical', durationMs: 500 }],
    unsupportedWords: ['test'],
    fingerspellingApplied: false
  });
  assert.strictEqual(Object.isFrozen(seq), true, 'SignSequence must be frozen');
  assert.strictEqual(Object.isFrozen(seq.signs), true, 'signs array must be frozen');
  assert.strictEqual(Object.isFrozen(seq.unsupportedWords), true, 'unsupportedWords array must be frozen');
  assert.strictEqual(seq.signs[0].gloss, 'YES');
  assert.strictEqual(Object.isFrozen(seq.signs[0]), true, 'sign items in sequence must be frozen');
});

// -----------------------------------------------------------------
// Suite 2: Missing Fields Enforcement
// -----------------------------------------------------------------
console.log('\n--- Suite 2: Missing Fields Enforcement ---');

runTest('Rejects SignItem missing gloss or empty gloss', () => {
  let res = C.validateSignItem({ category: 'lexical', durationMs: 500, source: 'seed_dictionary' });
  assert.strictEqual(res.valid, false);
  assert(res.errors.some(e => e.includes('gloss')), 'Error must mention gloss');

  res = C.validateSignItem({ gloss: '   ', category: 'lexical', durationMs: 500, source: 'seed_dictionary' });
  assert.strictEqual(res.valid, false);
});

runTest('Rejects SignItem missing category or durationMs or source', () => {
  let res = C.validateSignItem({ gloss: 'HELLO', durationMs: 500, source: 'seed_dictionary' });
  assert.strictEqual(res.valid, false);
  assert(res.errors.some(e => e.includes('category')));

  res = C.validateSignItem({ gloss: 'HELLO', category: 'lexical', source: 'seed_dictionary' });
  assert.strictEqual(res.valid, false);
  assert(res.errors.some(e => e.includes('durationMs')));

  res = C.validateSignItem({ gloss: 'HELLO', category: 'lexical', durationMs: 500 });
  assert.strictEqual(res.valid, false);
  assert(res.errors.some(e => e.includes('source')));
});

runTest('Rejects SignSequence missing sequenceId or language', () => {
  let res = C.validateSignSequence({
    language: 'ISL',
    rawTranscript: 'hi',
    sourceChunkSeq: 0,
    startMediaTimeMs: 0,
    endMediaTimeMs: 1000,
    signs: [],
    unsupportedWords: [],
    fingerspellingApplied: false
  });
  assert.strictEqual(res.valid, false);
  assert(res.errors.some(e => e.includes('sequenceId')));

  res = C.validateSignSequence({
    sequenceId: 'seq_1',
    rawTranscript: 'hi',
    sourceChunkSeq: 0,
    startMediaTimeMs: 0,
    endMediaTimeMs: 1000,
    signs: [],
    unsupportedWords: [],
    fingerspellingApplied: false
  });
  assert.strictEqual(res.valid, false);
  assert(res.errors.some(e => e.includes('language')));
});

runTest('Rejects SignSequence missing signs or unsupportedWords or fingerspellingApplied', () => {
  const base = {
    sequenceId: 'seq_1',
    language: 'ISL',
    rawTranscript: 'hi',
    sourceChunkSeq: 0,
    startMediaTimeMs: 0,
    endMediaTimeMs: 1000
  };
  let res = C.validateSignSequence({ ...base, unsupportedWords: [], fingerspellingApplied: false });
  assert.strictEqual(res.valid, false);
  assert(res.errors.some(e => e.includes('signs')));

  res = C.validateSignSequence({ ...base, signs: [], fingerspellingApplied: false });
  assert.strictEqual(res.valid, false);
  assert(res.errors.some(e => e.includes('unsupportedWords')));

  res = C.validateSignSequence({ ...base, signs: [], unsupportedWords: [] });
  assert.strictEqual(res.valid, false);
  assert(res.errors.some(e => e.includes('fingerspellingApplied')));
});

// -----------------------------------------------------------------
// Suite 3: Allowed Enum Values & Consistency Rules
// -----------------------------------------------------------------
console.log('\n--- Suite 3: Allowed Enum Values & Consistency Rules ---');

runTest('Rejects invalid SignItem category', () => {
  const res = C.validateSignItem({
    gloss: 'HELLO',
    category: 'unknown_category',
    durationMs: 500,
    source: 'seed_dictionary'
  });
  assert.strictEqual(res.valid, false);
  assert(res.errors.some(e => e.includes('category')));
});

runTest('Rejects invalid SignItem source', () => {
  const res = C.validateSignItem({
    gloss: 'HELLO',
    category: 'lexical',
    durationMs: 500,
    source: 'remote_cloud_api'
  });
  assert.strictEqual(res.valid, false);
  assert(res.errors.some(e => e.includes('source')));
});

runTest('Rejects invalid SignSequence language', () => {
  const res = C.validateSignSequence({
    sequenceId: 'seq_1',
    language: 'FRENCH_SIGN',
    rawTranscript: 'bonjour',
    sourceChunkSeq: 0,
    startMediaTimeMs: 0,
    endMediaTimeMs: 1000,
    signs: [],
    unsupportedWords: [],
    fingerspellingApplied: false
  });
  assert.strictEqual(res.valid, false);
  assert(res.errors.some(e => e.includes('language')));
});

runTest('Rejects invalid nonManualMarker enums', () => {
  const res = C.validateSignItem({
    gloss: 'HELLO',
    category: 'lexical',
    durationMs: 500,
    source: 'seed_dictionary',
    nonManualMarker: {
      headTilt: 'upside_down',
      eyebrows: 'winking'
    }
  });
  assert.strictEqual(res.valid, false);
  assert(res.errors.some(e => e.includes('headTilt')));
  assert(res.errors.some(e => e.includes('eyebrows')));
});

runTest('Enforces consistency between category and source', () => {
  let res = C.validateSignItem({
    gloss: 'A',
    category: 'fingerspelling',
    durationMs: 300,
    source: 'seed_dictionary'
  });
  assert.strictEqual(res.valid, false);

  res = C.validateSignItem({
    gloss: 'PAUSE',
    category: 'pause',
    durationMs: 300,
    source: 'seed_dictionary'
  });
  assert.strictEqual(res.valid, false);
});

// -----------------------------------------------------------------
// Suite 4: Duration & Timestamp Range Boundaries
// -----------------------------------------------------------------
console.log('\n--- Suite 4: Duration & Timestamp Boundaries ---');

runTest('Rejects negative or non-finite durationMs in SignItem', () => {
  let res = C.validateSignItem({
    gloss: 'HELLO',
    category: 'lexical',
    durationMs: -500,
    source: 'seed_dictionary'
  });
  assert.strictEqual(res.valid, false);
  assert(res.errors.some(e => e.includes('durationMs')));

  res = C.validateSignItem({
    gloss: 'HELLO',
    category: 'lexical',
    durationMs: Infinity,
    source: 'seed_dictionary'
  });
  assert.strictEqual(res.valid, false);
  assert(res.errors.some(e => e.includes('durationMs')));
});

runTest('Rejects negative timestamps in SignSequence', () => {
  const res = C.validateSignSequence({
    sequenceId: 'seq_1',
    language: 'ISL',
    rawTranscript: 'hi',
    sourceChunkSeq: 0,
    startMediaTimeMs: -100,
    endMediaTimeMs: 1000,
    signs: [],
    unsupportedWords: [],
    fingerspellingApplied: false
  });
  assert.strictEqual(res.valid, false);
  assert(res.errors.some(e => e.includes('startMediaTimeMs')));
});

runTest('Rejects endMediaTimeMs less than startMediaTimeMs', () => {
  const res = C.validateSignSequence({
    sequenceId: 'seq_1',
    language: 'ISL',
    rawTranscript: 'hi',
    sourceChunkSeq: 0,
    startMediaTimeMs: 2500,
    endMediaTimeMs: 1000,
    signs: [],
    unsupportedWords: [],
    fingerspellingApplied: false
  });
  assert.strictEqual(res.valid, false);
  assert(res.errors.some(e => e.includes('endMediaTimeMs')));
});

runTest('Accepts equal startMediaTimeMs and endMediaTimeMs (zero-duration boundary)', () => {
  const res = C.validateSignSequence({
    sequenceId: 'seq_zero',
    language: 'ISL',
    rawTranscript: '',
    sourceChunkSeq: 0,
    startMediaTimeMs: 1000,
    endMediaTimeMs: 1000,
    signs: [],
    unsupportedWords: [],
    fingerspellingApplied: false
  });
  assert.strictEqual(res.valid, true);
});

// -----------------------------------------------------------------
// Suite 5: Empty Sequences & Child Validation
// -----------------------------------------------------------------
console.log('\n--- Suite 5: Empty Sequences & Child Validation ---');

runTest('Accepts valid empty sequence (silence / no speech)', () => {
  const res = C.validateSignSequence({
    sequenceId: 'seq_silent',
    language: 'ISL',
    rawTranscript: '',
    sourceChunkSeq: 5,
    startMediaTimeMs: 10000,
    endMediaTimeMs: 12000,
    signs: [],
    unsupportedWords: [],
    fingerspellingApplied: false
  });
  assert.strictEqual(res.valid, true);
});

runTest('Recursively detects and reports invalid child SignItems inside sequence', () => {
  const res = C.validateSignSequence({
    sequenceId: 'seq_bad_child',
    language: 'ISL',
    rawTranscript: 'hello',
    sourceChunkSeq: 1,
    startMediaTimeMs: 0,
    endMediaTimeMs: 2000,
    signs: [
      { gloss: 'VALID', category: 'lexical', durationMs: 500, source: 'seed_dictionary' },
      { gloss: 'INVALID', category: 'lexical', durationMs: -200, source: 'seed_dictionary' }
    ],
    unsupportedWords: [],
    fingerspellingApplied: false
  });
  assert.strictEqual(res.valid, false);
  assert(res.errors.some(e => e.includes('signs[1]') && e.includes('durationMs')));
});

// -----------------------------------------------------------------
// Suite 6: Unsupported Words & Honest Telemetry
// -----------------------------------------------------------------
console.log('\n--- Suite 6: Unsupported Words & Honest Telemetry ---');

runTest('Accepts string list of unsupported words', () => {
  const res = C.validateSignSequence({
    sequenceId: 'seq_unsupported',
    language: 'ISL',
    rawTranscript: 'today we explore quantum thermodynamics',
    sourceChunkSeq: 2,
    startMediaTimeMs: 4000,
    endMediaTimeMs: 6000,
    signs: [{ gloss: 'TODAY', category: 'lexical', durationMs: 600, source: 'seed_dictionary' }],
    unsupportedWords: ['quantum', 'thermodynamics'],
    fingerspellingApplied: false
  });
  assert.strictEqual(res.valid, true);
});

runTest('Rejects non-string items or empty strings in unsupportedWords', () => {
  let res = C.validateSignSequence({
    sequenceId: 'seq_bad_unsupported',
    language: 'ISL',
    rawTranscript: 'test',
    sourceChunkSeq: 1,
    startMediaTimeMs: 0,
    endMediaTimeMs: 2000,
    signs: [],
    unsupportedWords: ['valid', 12345],
    fingerspellingApplied: false
  });
  assert.strictEqual(res.valid, false);

  res = C.validateSignSequence({
    sequenceId: 'seq_bad_unsupported_2',
    language: 'ISL',
    rawTranscript: 'test',
    sourceChunkSeq: 1,
    startMediaTimeMs: 0,
    endMediaTimeMs: 2000,
    signs: [],
    unsupportedWords: ['   '],
    fingerspellingApplied: false
  });
  assert.strictEqual(res.valid, false);
});

// -----------------------------------------------------------------
// Suite 7: Fingerspelling Constraints & Metadata
// -----------------------------------------------------------------
console.log('\n--- Suite 7: Fingerspelling Constraints & Metadata ---');

runTest('Accepts single-character gloss for fingerspelling', () => {
  const item = {
    gloss: 'K',
    category: 'fingerspelling',
    durationMs: 350,
    source: 'fingerspell_fallback'
  };
  const res = C.validateSignItem(item);
  assert.strictEqual(res.valid, true);
});

runTest('Rejects multi-character gloss for fingerspelling category', () => {
  const item = {
    gloss: 'APPLE',
    category: 'fingerspelling',
    durationMs: 350,
    source: 'fingerspell_fallback'
  };
  const res = C.validateSignItem(item);
  assert.strictEqual(res.valid, false);
  assert(res.errors.some(e => e.includes('single-character gloss')));
});

runTest('Enforces boolean type for fingerspellingApplied', () => {
  const res = C.validateSignSequence({
    sequenceId: 'seq_fs_bool',
    language: 'ISL',
    rawTranscript: 'test',
    sourceChunkSeq: 1,
    startMediaTimeMs: 0,
    endMediaTimeMs: 2000,
    signs: [],
    unsupportedWords: [],
    fingerspellingApplied: 'true'
  });
  assert.strictEqual(res.valid, false);
  assert(res.errors.some(e => e.includes('fingerspellingApplied')));
});

// -----------------------------------------------------------------
// Suite 8: Animation Identifier Contract & Validation
// -----------------------------------------------------------------
console.log('\n--- Suite 8: Animation Identifier Contract & Validation ---');

runTest('Accepts valid animationId string matching alphanumeric/dash/underscore/dot', () => {
  const item = {
    gloss: 'PLEASE',
    category: 'lexical',
    durationMs: 700,
    source: 'seed_dictionary',
    animationId: 'anim_isl_please_v1.0'
  };
  const res = C.validateSignItem(item);
  assert.strictEqual(res.valid, true);
});

runTest('Accepts null or omitted animationId (decoupling linguistic gloss from asset registry)', () => {
  const res1 = C.validateSignItem({
    gloss: 'HELLO',
    category: 'lexical',
    durationMs: 600,
    source: 'seed_dictionary',
    animationId: null
  });
  assert.strictEqual(res1.valid, true);

  const res2 = C.validateSignItem({
    gloss: 'HELLO',
    category: 'lexical',
    durationMs: 600,
    source: 'seed_dictionary'
  });
  assert.strictEqual(res2.valid, true);
});

runTest('Rejects invalid animationId with whitespace or disallowed characters', () => {
  const res = C.validateSignItem({
    gloss: 'HELLO',
    category: 'lexical',
    durationMs: 600,
    source: 'seed_dictionary',
    animationId: 'anim hello with spaces!'
  });
  assert.strictEqual(res.valid, false);
  assert(res.errors.some(e => e.includes('animationId')));
});

// -----------------------------------------------------------------
// Suite 9: Dependent Script Loading Verification
// -----------------------------------------------------------------
console.log('\n--- Suite 9: Dependent Script Loading Verification ---');

runTest('Loads ISLTranslator without missing dependency exception', () => {
  const isl = require('../translation/isl_translator.js');
  assert.strictEqual(typeof isl.translateTranscriptToISL, 'function');
  const seq = isl.translateTranscriptToISL('hello namaste thank you');
  assert.strictEqual(seq.language, 'ISL');
  assert.strictEqual(seq.signs.length, 3);
  const val = C.validateSignSequence(seq);
  assert.strictEqual(val.valid, true);
});

runTest('Loads ASLTranslator without missing dependency exception', () => {
  const asl = require('../translation/asl_translator.js');
  assert.strictEqual(typeof asl.translateTranscriptToASL, 'function');
  const seq = asl.translateTranscriptToASL('hello');
  assert.strictEqual(seq.language, 'ASL');
  assert.strictEqual(seq.unsupportedWords.length, 1);
  const val = C.validateSignSequence(seq);
  assert.strictEqual(val.valid, true);
});

runTest('Loads TranslationRouter without missing dependency exception', () => {
  const router = require('../translation/translation_router.js');
  assert.strictEqual(typeof router.routeTranscriptTranslation, 'function');
  const seq = router.routeTranscriptTranslation('welcome please', 'ISL');
  assert.strictEqual(seq.signs.length, 2);
  const val = C.validateSignSequence(seq);
  assert.strictEqual(val.valid, true);
});

runTest('Loads KeyframeRegistry without missing dependency exception', () => {
  const kf = require('../animation/keyframe_registry.js');
  assert.strictEqual(typeof kf.resolveSignAnimation, 'function');
  const signItem = C.createSignItem({
    gloss: 'NAMASTE',
    category: 'lexical',
    durationMs: 1800,
    source: 'seed_dictionary',
    animationId: 'isl_namaste_godl_v1'
  });
  const resolved = kf.resolveSignAnimation(signItem);
  assert.strictEqual(resolved.resolved, true);
  assert.strictEqual(resolved.isLinguisticISL, true);
});

// -----------------------------------------------------------------
// Suite 10: Sign Coverage, Decoupled Assets & Safe Fallback Verification (M8)
// -----------------------------------------------------------------
console.log('\n--- Suite 10: Sign Coverage, Decoupled Assets & Safe Fallback Verification (M8) ---');

runTest('Lexicon contains 16 glosses: 1 animated baseline and 15 un-animated entries with animationId: null', () => {
  const isl = require('../translation/isl_translator.js');
  const keys = Object.keys(isl.SEED_LEXICON);
  assert.strictEqual(keys.length, 16);
  assert.strictEqual(isl.SEED_LEXICON.NAMASTE.animationId, 'isl_namaste_godl_v1');
  
  const unanimated = keys.filter(k => k !== 'NAMASTE');
  assert.strictEqual(unanimated.length, 15);
  for (const k of unanimated) {
    assert.strictEqual(isl.SEED_LEXICON[k].animationId, undefined, `Gloss ${k} must not have animationId defined`);
  }
});

runTest('Un-animated dictionary gloss resolves to resolved: false and pose_neutral_rest_v1', () => {
  const kf = require('../animation/keyframe_registry.js');
  const signItem = C.createSignItem({
    gloss: 'HELLO',
    category: 'lexical',
    durationMs: 700,
    source: 'seed_dictionary',
    animationId: null
  });
  const res = kf.resolveSignAnimation(signItem);
  assert.strictEqual(res.resolved, false);
  assert.strictEqual(res.clip, null);
  assert.strictEqual(res.isLinguisticISL, false);
  assert.strictEqual(res.fallbackPose.poseId, 'pose_neutral_rest_v1');
  assert(res.reason.includes("No registered 3D animation clip exists"));
});

runTest('Non-existent animationId resolves safely to resolved: false without throwing', () => {
  const kf = require('../animation/keyframe_registry.js');
  const signItem = C.createSignItem({
    gloss: 'UNKNOWN_SIGN',
    category: 'lexical',
    durationMs: 500,
    source: 'seed_dictionary',
    animationId: 'clip_does_not_exist_xyz'
  });
  const res = kf.resolveSignAnimation(signItem);
  assert.strictEqual(res.resolved, false);
  assert.strictEqual(res.clip, null);
  assert.strictEqual(res.fallbackPose.poseId, 'pose_neutral_rest_v1');
});

runTest('Production Namaste resolves with isLinguisticISL: true and experimental_awaiting_validation', () => {
  const kf = require('../animation/keyframe_registry.js');
  const signItem = C.createSignItem({
    gloss: 'NAMASTE',
    category: 'lexical',
    durationMs: 1800,
    source: 'seed_dictionary',
    animationId: 'isl_namaste_godl_v1'
  });
  const res = kf.resolveSignAnimation(signItem);
  assert.strictEqual(res.resolved, true);
  assert.strictEqual(res.clip.animationId, 'isl_namaste_godl_v1');
  assert.strictEqual(res.clip.isLinguisticISL, true);
  assert.strictEqual(res.clip.validationStatus, 'experimental_awaiting_validation');
});

runTest('Partially supported phrase accurately partitions dictionary signs from unsupported words', () => {
  const isl = require('../translation/isl_translator.js');
  const seq = isl.translateTranscriptToISL('She makes me very, very proud.');
  assert.strictEqual(seq.signs.length, 1);
  assert.strictEqual(seq.signs[0].gloss, 'I');
  assert.strictEqual(seq.signs[0].animationId, null);
  assert.deepStrictEqual(seq.unsupportedWords, ['she', 'makes', 'very', 'very', 'proud']);
});

console.log('\n===============================================================');
console.log(` ALL ${passedTests} OF ${totalTests} CONTRACT TESTS PASSED CLEANLY!`);
console.log('===============================================================');


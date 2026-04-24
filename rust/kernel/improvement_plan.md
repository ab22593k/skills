# Rust Kernel Skill Improvement Plan

## Current State Analysis

The existing "Rust Kernel" skill has:
- ✅ Strong description with clear triggers
- ✅ Comprehensive reference materials (coding standards, API reference, debugging guide, etc.)
- ✅ Existing trigger_eval.json with 19 test cases (10 should trigger, 9 should not)
- ⚠️ SKILL.md could be more "pushy" to reduce undertriggering
- ⚠️ No validation/optimization loop established
- ⚠️ No automated testing framework

## Improvement Goals

1. **Optimize triggering logic** - Make the description more specific to reduce undertriggering
2. **Add validation framework** - Implement test suite with automated validation
3. **Create improvement loop** - Establish eval-viewer/generate_review.py workflow
4. **Add concrete examples** - More specific use cases in the description

## Specific Changes Needed

### 1. SKILL.md Description Optimization
Current description is good but could be more specific about:
- Concrete scenarios (module types: character, block, network devices)
- Specific error conditions (compilation failures, runtime panics)
- Explicit mention of "Rust For Linux" project
- More assertive language about when to use this skill

### 2. Test Suite Enhancement
- Add more diverse test cases covering:
  - Different module types (char, block, network)
  - Error handling scenarios
  - FFI and C interop
  - Debugging situations
  - Patch review cases

### 3. Validation Framework
- Copy scripts from skill-creator (run_loop.py, run_eval.py, etc.)
- Create proper test_cases.json structure
- Implement quick validation

## Implementation Steps

### Phase 1: Description Optimization (Priority: HIGH)
1. Analyze current trigger_eval.json to identify gaps
2. Rewrite SKILL.md description with more specific triggers
3. Add concrete kernel development scenarios

### Phase 2: Test Suite Expansion (Priority: MEDIUM)
1. Analyze existing 19 test cases
2. Add 10-15 more diverse test cases
3. Ensure coverage of all major kernel Rust use cases

### Phase 3: Validation Setup (Priority: MEDIUM)
1. Copy validation scripts to kernel directory
2. Create test_cases.json with proper format
3. Run quick validation

### Phase 4: Full Evaluation Loop (Priority: LOW)
1. Run complete evaluation with eval-viewer
2. Analyze results
3. Iterate based on feedback

## Expected Outcomes

- Reduced undertriggering while maintaining precision
- Automated validation of skill effectiveness
- Comprehensive test coverage for kernel Rust scenarios
- Clear improvement path based on data

## Risk Assessment

- Low risk: Description changes only affect triggering, not functionality
- Medium risk: Test expansion requires careful case design
- Low risk: Validation scripts are standard tooling

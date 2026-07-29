import test from 'node:test';
import assert from 'node:assert/strict';

import { shouldSkipCheckForPullRequest } from './check-changes-ownership.ts';

test('skips ownership check for triage:accepted:ready PRs', () => {
    assert.equal(shouldSkipCheckForPullRequest({
        labels: [{ name: 'triage:accepted:ready' }],
        title: 'feat: update span names',
    }), true);
});

test('skips ownership check for triage:accepted:ready-with-sig PRs', () => {
    assert.equal(shouldSkipCheckForPullRequest({
        labels: [{ name: 'triage:accepted:ready-with-sig' }],
        title: 'feat: update span names',
    }), true);
});

test('skips ownership check for chore PRs', () => {
    assert.equal(shouldSkipCheckForPullRequest({
        labels: [],
        title: '[chore] refresh generated files',
    }), true);
});

test('does not skip ownership check for unrelated PRs', () => {
    assert.equal(shouldSkipCheckForPullRequest({
        labels: [{ name: 'area:http' }],
        title: 'feat: add a new HTTP attribute',
    }), false);
});

test('does not skip ownership check for dependency PRs in script logic', () => {
    assert.equal(shouldSkipCheckForPullRequest({
        labels: [{ name: 'dependencies' }],
        title: 'chore(deps): update actions/checkout action to v7',
    }), false);
});

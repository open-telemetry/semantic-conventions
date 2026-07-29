import test from 'node:test';
import assert from 'node:assert/strict';

import { shouldSkipCheckForPullRequest } from './check-changes-ownership.ts';

test('skips ownership check for dependency PRs', () => {
    assert.equal(shouldSkipCheckForPullRequest({
        labels: [{ name: 'dependencies' }],
        title: 'chore(deps): update actions/checkout action to v7',
    }), true);
});

test('skips ownership check for accepted PRs and chore PRs', () => {
    assert.equal(shouldSkipCheckForPullRequest({
        labels: [{ name: 'triage:accepted:ready' }],
        title: 'feat: update span names',
    }), true);
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

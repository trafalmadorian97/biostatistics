"""
Given target assets, the scheduler is responsible for traversing the dependency graph consisting of the target assets and their transitive dependencies.

Delegates the actual work of materializing an individual asset up to date to the rebuilder.
"""

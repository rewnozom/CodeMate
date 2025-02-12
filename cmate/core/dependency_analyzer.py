# ..\..\cmate\core\dependency_analyzer.py
# cmate/core/dependency_analyzer.py
"""
cmate/core/dependency_analyzer.py

Implements advanced dependency analysis for different component types,
handling both direct and indirect dependencies with support for:
- Python imports and module dependencies
- Frontend dependencies (CSS, JS, templates)
- Configuration file relationships
- Circular dependency detection
"""

from dataclasses import dataclass, field
from typing import Dict, List, Optional, Set, Any
from pathlib import Path
from datetime import datetime
import ast
import re
import logging

from ..file_services.file_analyzer import FileAnalyzer, CodeAnalysis
from ..utils.error_handler import ErrorHandler

logger = logging.getLogger(__name__)
logger.info("Initializing ComponentDependencyAnalyzer.")

@dataclass
class DependencyInfo:
    """Information about a component's dependencies"""
    direct_deps: List[Path]
    indirect_deps: List[Path]
    reverse_deps: List[Path]  # Components that depend on this one
    circular_deps: List[List[Path]]  # Lists of circular dependency chains
    weight: int  # Dependency complexity weight
    metadata: Dict[str, Any] = field(default_factory=dict)
    timestamp: datetime = field(default_factory=datetime.now)

@dataclass
class DependencyGraph:
    """Represents the project's dependency structure"""
    nodes: Dict[Path, Set[Path]]  # Direct dependencies
    reverse_nodes: Dict[Path, Set[Path]]  # Reverse dependencies
    weights: Dict[Path, int]  # Node weights
    metadata: Dict[str, Any] = field(default_factory=dict)

class ComponentDependencyAnalyzer:
    """Analyzes component dependencies across the project"""
    
    def __init__(self, workspace_path: Optional[str] = None):
        self.workspace = Path(workspace_path) if workspace_path else Path("./Workspace")
        self.file_analyzer = FileAnalyzer()
        self.error_handler = ErrorHandler()
        self.dependency_cache: Dict[Path, DependencyInfo] = {}
        self.graph = DependencyGraph(
            nodes={},
            reverse_nodes={},
            weights={},
            metadata={"last_update": datetime.now()}
        )
        logger.info("ComponentDependencyAnalyzer initialized with workspace: %s", self.workspace)
        logger.success("ComponentDependencyAnalyzer initialized successfully with workspace: %s", self.workspace)

    async def analyze_dependencies(self, component_path: Path) -> DependencyInfo:
        """Analyze all dependencies for a component"""
        logger.info("Starting dependency analysis for component: %s", component_path)
        try:
            # Check cache first
            if component_path in self.dependency_cache:
                if self._is_cache_valid(component_path):
                    logger.debug("Cache hit for component: %s", component_path)
                    logger.success("Using cached dependency analysis for %s", component_path)
                    return self.dependency_cache[component_path]

            # Get file analysis
            analysis = await self.file_analyzer.analyze_file(component_path)
            logger.debug("File analysis completed for component: %s, file type: %s", component_path, analysis.file_type)
            
            # Extract direct dependencies
            direct_deps = await self._get_direct_dependencies(component_path, analysis)
            logger.debug("Direct dependencies for %s: %s", component_path, direct_deps)
            
            # Build dependency graph for this component
            self._update_graph(component_path, direct_deps)
            logger.debug("Dependency graph updated for component: %s", component_path)
            
            # Get indirect dependencies
            indirect_deps = self._get_indirect_dependencies(component_path)
            # Find reverse dependencies
            reverse_deps = list(self.graph.reverse_nodes.get(component_path, set()))
            # Detect circular dependencies
            circular_deps = self._detect_circular_dependencies(component_path)
            # Calculate dependency weight
            weight = self._calculate_dependency_weight(component_path, direct_deps, indirect_deps, circular_deps)
            logger.info("Dependency analysis complete for %s; weight: %d", component_path, weight)
            
            dep_info = DependencyInfo(
                direct_deps=direct_deps,
                indirect_deps=indirect_deps,
                reverse_deps=reverse_deps,
                circular_deps=circular_deps,
                weight=weight,
                metadata={
                    "file_type": analysis.file_type,
                    "complexity": analysis.code_analysis.complexity if analysis.code_analysis else 0
                }
            )
            self.dependency_cache[component_path] = dep_info
            logger.success("Dependency analysis stored successfully for %s", component_path)
            return dep_info
        except Exception as e:
            self.error_handler.handle_error(e, severity=self.error_handler.logger.level, metadata={"component": str(component_path)})
            raise

    async def _get_direct_dependencies(self, component_path: Path, analysis: CodeAnalysis) -> List[Path]:
        """Get direct dependencies based on file type"""
        deps = set()
        if component_path.suffix == '.py':
            deps.update(await self._analyze_python_deps(component_path, analysis))
        elif component_path.suffix in {'.html', '.js'}:
            deps.update(await self._analyze_frontend_deps(component_path, analysis))
        elif component_path.suffix in {'.yaml', '.yml', '.json'}:
            deps.update(await self._analyze_config_deps(component_path, analysis))
        return list(deps)

    async def _analyze_python_deps(self, file_path: Path, analysis: CodeAnalysis) -> Set[Path]:
        """Analyze Python file dependencies"""
        deps = set()
        logger.debug("Analyzing Python dependencies for file: %s", file_path)
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                tree = ast.parse(f.read())
            for node in ast.walk(tree):
                if isinstance(node, ast.Import):
                    for name in node.names:
                        dep_path = self._resolve_import(name.name)
                        if dep_path:
                            deps.add(dep_path)
                elif isinstance(node, ast.ImportFrom):
                    if node.module:
                        dep_path = self._resolve_import(node.module)
                        if dep_path:
                            deps.add(dep_path)
        except Exception as e:
            self.error_handler.handle_error(e, metadata={"file": str(file_path)})
        return deps

    async def _analyze_frontend_deps(self, file_path: Path, analysis: CodeAnalysis) -> Set[Path]:
        """Analyze frontend file dependencies"""
        deps = set()
        logger.debug("Analyzing frontend dependencies for file: %s", file_path)
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            css_deps = re.findall(r'href=[\'"]([^\'"]+\.css)[\'"]', content)
            deps.update(self._resolve_frontend_paths(file_path, css_deps))
            js_deps = re.findall(r'src=[\'"]([^\'"]+\.js)[\'"]', content)
            deps.update(self._resolve_frontend_paths(file_path, js_deps))
            template_deps = re.findall(r'{%\s*include\s+[\'"]([^\'"]+)[\'"]', content)
            deps.update(self._resolve_frontend_paths(file_path, template_deps))
        except Exception as e:
            self.error_handler.handle_error(e, metadata={"file": str(file_path)})
        return deps

    async def _analyze_config_deps(self, file_path: Path, analysis: CodeAnalysis) -> Set[Path]:
        """Analyze configuration file dependencies"""
        deps = set()
        logger.debug("Analyzing configuration dependencies for file: %s", file_path)
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            file_refs = re.findall(r'file:\s*[\'"]([^\'"]+)[\'"]', content)
            deps.update(self._resolve_config_paths(file_path, file_refs))
            path_refs = re.findall(r'path:\s*[\'"]([^\'"]+)[\'"]', content)
            deps.update(self._resolve_config_paths(file_path, path_refs))
        except Exception as e:
            self.error_handler.handle_error(e, metadata={"file": str(file_path)})
        return deps

    def _resolve_import(self, import_name: str) -> Optional[Path]:
        """Resolve Python import to actual file path"""
        parts = import_name.split('.')
        possible_paths = [
            self.workspace / '/'.join(parts) / '__init__.py',
            self.workspace / '/'.join(parts) + '.py'
        ]
        for path in possible_paths:
            if path.exists():
                logger.debug("Resolved import '%s' to path: %s", import_name, path)
                return path
        logger.debug("Could not resolve import: %s", import_name)
        return None

    def _resolve_frontend_paths(self, source_file: Path, references: List[str]) -> Set[Path]:
        """Resolve frontend file references to actual paths"""
        resolved = set()
        source_dir = source_file.parent
        for ref in references:
            if ref.startswith('./') or ref.startswith('../'):
                path = (source_dir / ref).resolve()
            else:
                path = (self.workspace / ref.lstrip('/')).resolve()
            if path.exists():
                resolved.add(path)
        return resolved

    def _resolve_config_paths(self, config_file: Path, references: List[str]) -> Set[Path]:
        """Resolve config file references to actual paths"""
        resolved = set()
        config_dir = config_file.parent
        for ref in references:
            path = (config_dir / ref).resolve()
            if not path.exists():
                path = (self.workspace / ref).resolve()
            if path.exists():
                resolved.add(path)
        return resolved

    def _update_graph(self, source: Path, dependencies: List[Path]) -> None:
        """Update dependency graph with new information"""
        if source not in self.graph.nodes:
            self.graph.nodes[source] = set()
        self.graph.nodes[source].update(dependencies)
        for dep in dependencies:
            if dep not in self.graph.reverse_nodes:
                self.graph.reverse_nodes[dep] = set()
            self.graph.reverse_nodes[dep].add(source)
        logger.debug("Updated dependency graph for component: %s", source)

    def _get_indirect_dependencies(self, component_path: Path) -> List[Path]:
        """Get all indirect dependencies"""
        indirect = set()
        visited = {component_path}
        def visit(path: Path):
            for dep in self.graph.nodes.get(path, set()):
                if dep not in visited:
                    visited.add(dep)
                    indirect.add(dep)
                    visit(dep)
        visit(component_path)
        return list(indirect)

    def _detect_circular_dependencies(self, start_path: Path) -> List[List[Path]]:
        """Detect circular dependencies starting from a component"""
        circular_deps = []
        visited = set()
        path_stack = []
        def visit(current_path: Path):
            if current_path in path_stack:
                cycle_start = path_stack.index(current_path)
                circular_deps.append(path_stack[cycle_start:] + [current_path])
                return
            if current_path in visited:
                return
            visited.add(current_path)
            path_stack.append(current_path)
            for dep in self.graph.nodes.get(current_path, set()):
                visit(dep)
            path_stack.pop()
        visit(start_path)
        return circular_deps

    def _calculate_dependency_weight(self, component_path: Path, direct_deps: List[Path], indirect_deps: List[Path], circular_deps: List[List[Path]]) -> int:
        """Calculate dependency complexity weight"""
        weight = 0
        weight += len(direct_deps) * 2
        weight += len(indirect_deps)
        weight += len(circular_deps) * 5
        if component_path.suffix == '.py':
            weight += 2
        elif component_path.suffix in {'.html', '.js'}:
            weight += 1
        return weight

    def _is_cache_valid(self, component_path: Path) -> bool:
        """Check if cached dependency info is still valid"""
        if component_path not in self.dependency_cache:
            return False
        cache_entry = self.dependency_cache[component_path]
        file_mtime = datetime.fromtimestamp(component_path.stat().st_mtime)
        valid = (file_mtime < cache_entry.timestamp and (datetime.now() - cache_entry.timestamp).total_seconds() < 3600)
        logger.debug("Cache valid for %s: %s", component_path, valid)
        return valid

    def get_dependency_stats(self) -> Dict[str, Any]:
        """Get statistics about project dependencies"""
        stats = {
            "total_components": len(self.graph.nodes),
            "total_dependencies": sum(len(deps) for deps in self.graph.nodes.values()),
            "circular_dependencies": sum(1 for deps in self.graph.nodes.values() if any(node in deps for node in deps)),
            "max_weight": max(self.graph.weights.values()) if self.graph.weights else 0,
            "isolated_components": sum(1 for deps in self.graph.nodes.values() if not deps and not self.graph.reverse_nodes.get(deps)),
            "last_update": self.graph.metadata["last_update"].isoformat()
        }
        logger.info("Dependency stats: %s", stats)
        return stats

    def clear_cache(self) -> None:
        """Clear dependency cache"""
        self.dependency_cache.clear()
        self.graph.metadata["last_update"] = datetime.now()
        logger.info("Cleared dependency cache.")
        logger.success("Dependency cache cleared successfully.")

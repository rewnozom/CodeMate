# ..\..\cmate\core\navigation_system.py
"""
cmate/core/navigation_system.py

Implements the NavigationDecisionSystem responsible for:
- Analyzing the workspace and files
- Classifying components
- Making navigation decisions
- Handling multi-component navigation
"""

from dataclasses import dataclass, field
from typing import Dict, List, Optional, Any
from pathlib import Path
from datetime import datetime
from uuid import UUID, uuid4
import logging

from ..core.state_manager import AgentState
from ..file_services.file_analyzer import FileAnalyzer
from ..file_services.workspace_scanner import WorkspaceScanner

logger = logging.getLogger(__name__)
logger.success("NavigationDecisionSystem module loaded successfully.")

@dataclass
class NavigationContext:
    """Context for navigation decisions"""
    request_id: UUID
    user_request: str
    current_path: Path
    target_components: List[Path]
    dependencies: Dict[Path, List[Path]]
    state_history: List[AgentState]
    metadata: Dict[str, Any] = field(default_factory=dict)

@dataclass
class NavigationResult:
    """Result of a navigation decision"""
    success: bool
    chosen_path: Optional[Path]
    component_type: str
    dependencies: List[Path]
    action_taken: str
    navigation_history: List[str]
    timestamp: datetime = field(default_factory=datetime.now)
    metadata: Dict[str, Any] = field(default_factory=dict)

class ComponentClassifier:
    """Classifies components based on content and structure"""
    
    def __init__(self):
        self.file_analyzer = FileAnalyzer()
        logger.debug("ComponentClassifier initialized.")

    async def classify_component(self, file_path: Path) -> str:
        """Classify a component based on its content and file path"""
        logger.debug("Classifying component: %s", file_path)
        analysis = await self.file_analyzer.analyze_file(file_path)
        if "test" in file_path.stem.lower():
            logger.debug("Component classified as TEST based on filename.")
            return "TEST"
        elif analysis.file_type == ".py":
            if self._is_backend_code(analysis):
                logger.debug("Component classified as BACKEND.")
                return "BACKEND"
            elif self._is_frontend_code(analysis):
                logger.debug("Component classified as FRONTEND.")
                return "FRONTEND"
        elif analysis.file_type in [".html", ".css", ".js"]:
            logger.debug("Component classified as FRONTEND based on file type.")
            return "FRONTEND"
        elif analysis.file_type in [".json", ".yaml", ".yml"]:
            logger.debug("Component classified as CONFIG based on file type.")
            return "CONFIG"
        logger.debug("Component classified as UNKNOWN.")
        return "UNKNOWN"
        
    def _is_backend_code(self, analysis: Any) -> bool:
        """Check if the code is backend-related"""
        backend_indicators = [
            "django", "flask", "fastapi", "sqlalchemy",
            "database", "model", "schema", "api"
        ]
        return any(ind in str(analysis.imports).lower() for ind in backend_indicators)
        
    def _is_frontend_code(self, analysis: Any) -> bool:
        """Check if the code is frontend-related"""
        frontend_indicators = [
            "template", "html", "css", "javascript",
            "react", "vue", "angular", "dom"
        ]
        return any(ind in str(analysis.imports).lower() for ind in frontend_indicators)

class NavigationDecisionSystem:
    """Main system for making navigation decisions"""
    
    def __init__(self, workspace_path: Optional[str] = None):
        self.workspace = Path(workspace_path) if workspace_path else Path("./Workspace")
        self.scanner = WorkspaceScanner(str(self.workspace))
        self.classifier = ComponentClassifier()
        self.current_context: Optional[NavigationContext] = None
        logger.info("NavigationDecisionSystem initialized with workspace: %s", self.workspace)
        logger.success("NavigationDecisionSystem initialized successfully.")

    async def prepare_decision_context(
        self,
        request: str,
        workspace_data: dict,
        current_state: AgentState
    ) -> NavigationContext:
        """
        Prepare the navigation decision context based on:
          - The user's request
          - Workspace analysis
          - Current state
        """
        logger.info("Preparing navigation context for request: %s", request)
        context_id = uuid4()
        current_path = self.workspace
        
        # Scan the workspace
        scan_result = await self.scanner.scan_workspace()
        logger.debug("Workspace scan complete. Total files found: %d", len(scan_result.files))
        
        # Identify target components
        target_components = []
        for file_info in scan_result.files:
            if self._is_relevant_for_request(file_info, request):
                target_components.append(file_info.path)
        logger.debug("Target components identified: %s", target_components)
        
        # Analyze dependencies for each target component
        dependencies = {}
        for component in target_components:
            deps = await self._analyze_dependencies(component)
            dependencies[component] = deps
            logger.debug("Dependencies for %s: %s", component, deps)
            
        context = NavigationContext(
            request_id=context_id,
            user_request=request,
            current_path=current_path,
            target_components=target_components,
            dependencies=dependencies,
            state_history=[current_state],
            metadata=workspace_data
        )
        logger.info("Navigation context prepared with request_id: %s", context_id)
        logger.success("Navigation context prepared successfully with request_id: %s", context_id)
        return context
        
    def get_available_actions(self, context: NavigationContext) -> List[str]:
        """
        Return available navigation actions based on the context.
        For example: ['ANALYZE_FILE', 'CREATE_NEW', 'MODIFY_EXISTING']
        """
        actions = ["ANALYZE_FILE", "SCAN_DEPENDENCIES"]
        if context.target_components:
            actions.append("MODIFY_EXISTING")
        else:
            actions.append("CREATE_NEW")
        if len(context.target_components) > 1:
            actions.append("HANDLE_MULTIPLE")
        logger.debug("Available actions based on context: %s", actions)
        return actions
        
    async def execute_navigation(
        self,
        chosen_action: str,
        context: NavigationContext
    ) -> NavigationResult:
        """Execute the chosen navigation action"""
        logger.info("Executing navigation action: %s", chosen_action)
        try:
            if chosen_action == "ANALYZE_FILE":
                result = await self._execute_analysis(context)
            elif chosen_action == "CREATE_NEW":
                result = await self._execute_creation(context)
            elif chosen_action == "MODIFY_EXISTING":
                result = await self._execute_modification(context)
            elif chosen_action == "HANDLE_MULTIPLE":
                result = await self._execute_multi_handling(context)
            else:
                raise ValueError(f"Unknown action: {chosen_action}")
            logger.info("Navigation action '%s' executed successfully.", chosen_action)
            logger.success("Navigation action '%s' executed successfully.", chosen_action)
            return result
        except Exception as e:
            logger.error("Error executing navigation action '%s': %s", chosen_action, str(e))
            return NavigationResult(
                success=False,
                chosen_path=None,
                component_type="ERROR",
                dependencies=[],
                action_taken=chosen_action,
                navigation_history=[f"Error: {str(e)}"],
                metadata={"error": str(e)}
            )
            
    async def _execute_analysis(self, context: NavigationContext) -> NavigationResult:
        """Perform file analysis"""
        if not context.target_components:
            raise ValueError("No target components for analysis")
        target = context.target_components[0]
        component_type = await self.classifier.classify_component(target)
        logger.debug("Analysis executed on %s; classified as %s", target, component_type)
        logger.success("Analysis executed successfully on %s", target)
        return NavigationResult(
            success=True,
            chosen_path=target,
            component_type=component_type,
            dependencies=context.dependencies.get(target, []),
            action_taken="ANALYZE_FILE",
            navigation_history=[f"Analyzed {target}"],
            metadata={"analysis_type": component_type, "file_count": len(context.target_components)}
        )
        
    async def _execute_creation(self, context: NavigationContext) -> NavigationResult:
        """Prepare to create a new file"""
        target_path = self._determine_new_file_path(context.user_request)
        logger.debug("Determined new file path: %s", target_path)
        logger.success("Creation action prepared successfully with target path: %s", target_path)
        return NavigationResult(
            success=True,
            chosen_path=target_path,
            component_type="NEW",
            dependencies=[],
            action_taken="CREATE_NEW",
            navigation_history=[f"Preparing to create {target_path}"],
            metadata={"creation_type": self._determine_component_type(context.user_request)}
        )
        
    async def _execute_modification(self, context: NavigationContext) -> NavigationResult:
        """Prepare to modify an existing file"""
        target = context.target_components[0]
        component_type = await self.classifier.classify_component(target)
        logger.debug("Preparing to modify %s, classified as %s", target, component_type)
        logger.success("Modification action prepared successfully for %s", target)
        return NavigationResult(
            success=True,
            chosen_path=target,
            component_type=component_type,
            dependencies=context.dependencies.get(target, []),
            action_taken="MODIFY_EXISTING",
            navigation_history=[f"Preparing to modify {target}"],
            metadata={"modification_type": "UPDATE"}
        )
        
    async def _execute_multi_handling(self, context: NavigationContext) -> NavigationResult:
        """Handle multi-component navigation"""
        prioritized = self._prioritize_components(context.target_components)
        primary_target = prioritized[0]
        logger.debug("Multi-component handling: %d components, primary: %s", len(prioritized), primary_target)
        logger.success("Multi-component handling prepared successfully for primary target: %s", primary_target)
        return NavigationResult(
            success=True,
            chosen_path=primary_target,
            component_type="MULTI",
            dependencies=context.dependencies.get(primary_target, []),
            action_taken="HANDLE_MULTIPLE",
            navigation_history=[f"Multi-component handling: {len(prioritized)} files"],
            metadata={"component_count": len(prioritized), "components": [str(p) for p in prioritized]}
        )
        
    def _is_relevant_for_request(self, file_info: Any, request: str) -> bool:
        """Check if a file is relevant for the request"""
        request_lower = request.lower()
        file_name = file_info.path.name.lower()
        return any(keyword in file_name for keyword in request_lower.split())
        
    async def _analyze_dependencies(self, file_path: Path) -> List[Path]:
        """Analyze dependencies for a file"""
        logger.debug("Analyzing dependencies for: %s", file_path)
        analysis = await self.file_analyzer.analyze_file(file_path)
        dependencies = []
        if hasattr(analysis, 'imports'):
            for imp in analysis.imports:
                dep_path = self._import_to_path(imp)
                if dep_path and dep_path.exists():
                    dependencies.append(dep_path)
        logger.debug("Dependencies for %s: %s", file_path, dependencies)
        return dependencies
        
    def _import_to_path(self, import_name: str) -> Optional[Path]:
        """Convert an import name to a possible file path"""
        parts = import_name.split('.')
        possible_path = self.workspace.joinpath(*parts).with_suffix('.py')
        return possible_path if possible_path.exists() else None
        
    def _determine_new_file_path(self, request: str) -> Path:
        """Determine an appropriate path for a new file"""
        component_type = self._determine_component_type(request)
        base_name = self._generate_file_name(request)
        if component_type == "FRONTEND":
            return self.workspace / "frontend" / base_name
        elif component_type == "BACKEND":
            return self.workspace / "backend" / base_name
        elif component_type == "TEST":
            return self.workspace / "tests" / f"test_{base_name}"
        else:
            return self.workspace / base_name
            
    def _determine_component_type(self, request: str) -> str:
        """Determine component type based on the request"""
        request_lower = request.lower()
        if any(word in request_lower for word in ["test", "testing", "validate"]):
            return "TEST"
        elif any(word in request_lower for word in ["api", "database", "model", "backend"]):
            return "BACKEND"
        elif any(word in request_lower for word in ["ui", "interface", "frontend"]):
            return "FRONTEND"
        return "UNKNOWN"
        
    def _generate_file_name(self, request: str) -> str:
        """Generate a file name from the request"""
        words = request.lower().split()[:3]
        base_name = "_".join(word.strip() for word in words if word.isalnum())
        if self._determine_component_type(request) == "FRONTEND":
            return f"{base_name}.html"
        else:
            return f"{base_name}.py"
            
    def _prioritize_components(self, components: List[Path]) -> List[Path]:
        """Prioritize components for multi-handling"""
        def priority_score(path: Path) -> int:
            score = 0
            if path.suffix == ".py":
                score += 5
            if "test" in path.stem.lower():
                score -= 2
            if "main" in path.stem.lower():
                score += 3
            return score
        prioritized = sorted(components, key=priority_score, reverse=True)
        logger.debug("Prioritized components: %s", prioritized)
        return prioritized

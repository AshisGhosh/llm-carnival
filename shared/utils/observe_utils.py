import uuid
import functools
import asyncio
from langfuse import Langfuse

langfuse = Langfuse()

# Define the decorator factory
def langfuse_tracking(name, trace_id=None, trace_id_attr=None, parent_observation_id=None, parent_observation_id_attr=None, model=None, model_attr=None, model_parameters=None, metadata=None):
    def decorator(func):
        @functools.wraps(func)
        async def wrapper(self, *args, **kwargs):

            def get_nested_attr(obj, attr_path, default=None):
                current = obj
                for part in attr_path.split('.'):
                    current = getattr(current, part, default)
                    if current is default:
                        break
                return current
            
            actual_trace_id = trace_id if trace_id is not None else (get_nested_attr(self, trace_id_attr, None) if trace_id_attr else None)
            actual_parent_observation_id = parent_observation_id if parent_observation_id is not None else (get_nested_attr(self, parent_observation_id_attr, None) if parent_observation_id_attr else None)
            actual_model = model if model is not None else (get_nested_attr(self, model_attr, None) if model_attr else None)

            # Check if no kwargs is empty
            if not kwargs:
                raise ValueError("No kwargs for input provided")

            # Prepare input for the generation call
            input = kwargs

            # Start tracking
            generation = langfuse.generation(
                trace_id=actual_trace_id,
                parent_observation_id=actual_parent_observation_id,
                name=name,
                model=actual_model,
                model_parameters=model_parameters,
                input=input,
                metadata=metadata
            )
            try:
                # Call the decorated function
                result = await func(self, *args, **kwargs)
                # End tracking with success
                generation.end(output=result)
                return result
            except Exception as e:
                # Handle failure or exception by ending the tracking with error information
                generation.end(output={"success": False, "text": str(e)})
                print(f"langfuse_tracking - Error during generation: {e}")
                return False
        return wrapper
    return decorator

def start_trace(name, user_id="ashis", session_id=None, input=None, metadata=None, tags=None):
    trace = langfuse.trace(
            name=name,
            user_id=user_id,
            session_id = session_id if session_id else str(uuid.uuid4()),
            input = input,
            metadata = metadata,
            tags = tags           
        )
    return trace
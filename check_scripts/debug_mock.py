from unittest.mock import MagicMock, PropertyMock
import numpy as np

def test_mock_behavior():
    print("--- Testing Mock Behavior ---")
    mock_ds = MagicMock()
    mock_sub = MagicMock()
    sti_values = np.array([0.1, 0.2])
    
    # Approach 1: Assignment
    mock_sub.values = sti_values
    
    # Check direct access
    print(f"Direct mock_sub.values: {mock_sub.values}")
    
    # Link ds -> sub
    mock_ds.__getitem__.return_value = mock_sub
    
    sub = mock_ds["sti"]
    print(f"Retrieved sub via ds['sti']: {sub}")
    print(f"Is sub same as mock_sub? {sub is mock_sub}")
    
    print(f"sub.values: {sub.values}")
    
    try:
        flat = sub.values.flatten().tolist()
        print(f"Flat result: {flat}")
        print(f"Is list? {isinstance(flat, list)}")
    except Exception as e:
        print(f"Error accessing sub.values: {e}")

    print("\n--- Testing PropertyMock ---")
    mock_sub2 = MagicMock()
    type(mock_sub2).values = PropertyMock(return_value=sti_values)
    print(f"PropertyMock sub.values: {mock_sub2.values}")

if __name__ == "__main__":
    test_mock_behavior()

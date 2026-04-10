from loguru import logger

def link_worker_outputs(all_worker_data):
    """
    Links the 5 workers together by finding overlapping structural drifts.
    """
    master_map = {}
    
    for record in all_worker_data:
        seq_id = record['sequence_id']
        if seq_id not in master_map:
            master_map[seq_id] = []
        
        master_map[seq_id].append({
            'worker_id': record['worker_id'],
            'drift': record['drift'],
            'severity': record['severity']
        })
    
    # Identify the Lazarus Protocol signature (Where multiple workers agree)
    lazarus_candidates = {k: v for k, v in master_map.items() if len(v) > 1}
    
    logger.info(f"🔱 Linked {len(lazarus_candidates)} overlapping signatures across workers.")
    return lazarus_candidates

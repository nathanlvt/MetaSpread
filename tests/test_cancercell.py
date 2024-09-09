from metaspread.cancermodel import CancerModel
from metaspread.cancercell import CancerCell
import numpy as np
import pytest
#todo: model is not callable (duh! I think I cannot call a private variable (is it though?))
#todo: use tmp_path_facorty to create the model once, and use it for the rest of the tests

def test_phenotype(tmp_path) -> None:
    temp_simulation_folder = tmp_path / "test_simulation"
    temp_simulation_folder.mkdir()
    model = CancerModel(
        number_of_initial_cells=30,
        width=201,
        height=201,
        grids_number=2,
        max_steps=1000,
        data_collection_period=10,
        new_simulation_folder=temp_simulation_folder)
    
    assert model.data_collection_period == 10
    assert model.number_of_initial_cells==30
    assert model.width==201
    assert model.height==201
    assert model.grids_number==2
    assert model.max_steps==1000
    assert model.data_collection_period==10
    assert model.new_simulation_folder==temp_simulation_folder

    ccell_id = None
    grid_id = 1
    #add to the following line the keyword arguments for the cancer cell
    ccell = CancerCell(
        unique_id=ccell_id,
        model=model, 
        grid=model.grids[grid_id-1], 
        grid_id=grid_id, 
        phenotype="mesenchymal", 
        ecm=model.ecm[grid_id-1], 
        mmp2=model.mmp2[grid_id-1]
    )

    assert ccell.unique_id          == ccell_id
    assert ccell.model              == model
    assert ccell.grid               == model.grids[grid_id-1]
    assert ccell.grid_id            == grid_id
    assert ccell.phenotype          == "mesenchymal"
    assert np.array_equal(ccell.ecm, model.ecm[grid_id-1])
    assert np.array_equal(ccell.mmp2, model.mmp2[grid_id-1])

    
    for agent in model.schedule.agents:
        if agent.agent_type == "cell":
            assert  agent.unique_id  <   model.number_of_initial_cells
            assert  agent.model      ==  ccell.model
            assert  agent.grid       ==  ccell.grid
            assert  agent.grid_id    ==  ccell.grid_id
            assert (agent.phenotype  ==  "mesenchymal" or  agent.phenotype  ==  "epithelial" )
            assert  np.array_equal(agent.ecm , ccell.ecm)
            assert  np.array_equal(agent.mmp2, ccell.mmp2)


    
    
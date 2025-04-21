local map = function (keys, desc, func)
    vim.keymap.set('n', keys, func, { desc = desc })
end

-- vim.g.mypy_cfg = 'ops/tools/mypy.ini'
-- vim.g.flake8_cfg = 'ops/tools/flake8.ini'


-- DAP configurations
local dap = require('dap')
table.insert(dap.configurations.python, {
    justMyCode = false,
    type = 'python';
    request = 'launch';
    name = 'peltak version';
    program = '/Users/novo/src/work/mns/fae/.venv/bin/peltak';
    args = {'version'};
    cwd = "${workspaceFolder}";
})


-- Project specific keymaps
vim.api.nvim_create_user_command('Todos', function()
    vim.cmd(':TodoTelescope cwd=./src initial_mode=normal')
end, {})

map('<leader>todo', 'Show all todos', ':Todos<CR>')

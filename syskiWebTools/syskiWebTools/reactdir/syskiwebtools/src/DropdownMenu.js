import React, { useState } from 'react';

function DropdownMenu(){
    const [anchorEl, setAnchorEl] = React.useState(null);
        
    const handleMouseEnter = (event) => {
        setAnchorEl(event.currentTarget);
    };

    const handleClose = () => {
        setAnchorEl(null);
    };

    return (
        <div>
            <Button
                color="inherit"
                aria-controls="simple-menu"
                aria-haspopup="true"
                onMouseEnter={handleMouseEnter}
            >
                {title}
            </Button>
            <Menu
                id="simple-menu"
                anchorEl={anchorEl}
                open={Boolean(anchorEl)}
                onClose={handleClose}
                PaperProps={{
                    onMouseLeave: handleClose
                }}
            >
                {menuItems.map(item => (
                    <MenuItem key={item.label} onClick={() => {
                        setCurrentApi(item.api);
                        handleClose();
                    }}>
                        {item.label}
                    </MenuItem>
                ))}
            </Menu>
        </div>
    );
}
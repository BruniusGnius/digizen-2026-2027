<?php

// Solo configuración de frontend. No define rutas, controladores ni envíos.
return [
    'frontend' => [
        'mode' => env('DIGIZEN_FRONTEND_MODE', 'preview'),
        'leadEndpoint' => env('DIGIZEN_LEAD_ENDPOINT', ''),
        'checkout' => [
            'monthly' => env('DIGIZEN_CHECKOUT_MONTHLY', ''),
            'cycle' => env('DIGIZEN_CHECKOUT_CYCLE', ''),
            'cash' => env('DIGIZEN_CHECKOUT_CASH', ''),
        ],
    ],
];

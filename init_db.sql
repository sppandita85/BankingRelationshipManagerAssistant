-- Initialize Banking RM Agent Database
-- This script runs when PostgreSQL container starts for the first time

-- Create customers table
CREATE TABLE IF NOT EXISTS customers (
    customer_id VARCHAR(50) PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    phone VARCHAR(20),
    auth_token_hash VARCHAR(255) NOT NULL,
    tier VARCHAR(20) DEFAULT 'regular' CHECK (tier IN ('regular', 'premium', 'hni', 'vip')),
    account_status VARCHAR(20) DEFAULT 'active' CHECK (account_status IN ('active', 'suspended', 'frozen', 'closed')),
    last_login TIMESTAMP,
    failed_attempts INTEGER DEFAULT 0,
    locked_until TIMESTAMP,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create remittances table
CREATE TABLE IF NOT EXISTS remittances (
    id SERIAL PRIMARY KEY,
    customer_id VARCHAR(50) NOT NULL,
    reference_id VARCHAR(50) UNIQUE NOT NULL,
    amount DECIMAL(15,2) NOT NULL,
    currency VARCHAR(3) DEFAULT 'USD',
    sender_name VARCHAR(100) NOT NULL,
    sender_account VARCHAR(50),
    recipient_name VARCHAR(100) NOT NULL,
    recipient_account VARCHAR(50),
    recipient_bank VARCHAR(100),
    recipient_country VARCHAR(50) NOT NULL,
    status VARCHAR(20) DEFAULT 'pending' CHECK (status IN ('pending', 'processing', 'completed', 'failed', 'cancelled')),
    transaction_type VARCHAR(20) DEFAULT 'domestic' CHECK (transaction_type IN ('domestic', 'international', 'wire_transfer', 'ach')),
    purpose TEXT,
    exchange_rate DECIMAL(10,4),
    fees DECIMAL(10,2) DEFAULT 0,
    net_amount DECIMAL(15,2),
    initiated_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    processed_date TIMESTAMP,
    completed_date TIMESTAMP,
    failure_reason TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (customer_id) REFERENCES customers(customer_id)
);

-- Create indexes for better performance
CREATE INDEX IF NOT EXISTS idx_customers_email ON customers(email);
CREATE INDEX IF NOT EXISTS idx_customers_tier ON customers(tier);
CREATE INDEX IF NOT EXISTS idx_remittances_customer_id ON remittances(customer_id);
CREATE INDEX IF NOT EXISTS idx_remittances_reference_id ON remittances(reference_id);
CREATE INDEX IF NOT EXISTS idx_remittances_status ON remittances(status);
CREATE INDEX IF NOT EXISTS idx_remittances_initiated_date ON remittances(initiated_date);

-- Insert sample customers
INSERT INTO customers (customer_id, name, email, phone, auth_token_hash, tier, account_status) VALUES
('CUST001', 'John Smith', 'john.smith@email.com', '+1-555-0101', 'hashed_token_001', 'hni', 'active'),
('CUST002', 'Sarah Johnson', 'sarah.johnson@email.com', '+1-555-0102', 'hashed_token_002', 'premium', 'active'),
('CUST003', 'Michael Brown', 'michael.brown@email.com', '+1-555-0103', 'hashed_token_003', 'vip', 'active'),
('CUST004', 'Emily Davis', 'emily.davis@email.com', '+1-555-0104', 'hashed_token_004', 'regular', 'active'),
('CUST005', 'David Wilson', 'david.wilson@email.com', '+1-555-0105', 'hashed_token_005', 'hni', 'active'),
('CUST006', 'Lisa Anderson', 'lisa.anderson@email.com', '+1-555-0106', 'hashed_token_006', 'premium', 'active'),
('CUST007', 'Robert Taylor', 'robert.taylor@email.com', '+1-555-0107', 'hashed_token_007', 'regular', 'active'),
('CUST008', 'Jennifer Martinez', 'jennifer.martinez@email.com', '+1-555-0108', 'hashed_token_008', 'vip', 'active'),
('CUST009', 'William Garcia', 'william.garcia@email.com', '+1-555-0109', 'hashed_token_009', 'hni', 'active'),
('CUST010', 'Amanda Rodriguez', 'amanda.rodriguez@email.com', '+1-555-0110', 'hashed_token_010', 'premium', 'active'),
('CUST011', 'Christopher Lee', 'christopher.lee@email.com', '+1-555-0111', 'hashed_token_011', 'regular', 'active'),
('CUST012', 'Michelle White', 'michelle.white@email.com', '+1-555-0112', 'hashed_token_012', 'vip', 'active'),
('CUST013', 'Daniel Harris', 'daniel.harris@email.com', '+1-555-0113', 'hashed_token_013', 'hni', 'active'),
('CUST014', 'Ashley Clark', 'ashley.clark@email.com', '+1-555-0114', 'hashed_token_014', 'premium', 'active'),
('CUST015', 'Matthew Lewis', 'matthew.lewis@email.com', '+1-555-0115', 'hashed_token_015', 'regular', 'active')
ON CONFLICT (customer_id) DO NOTHING;

-- Insert sample remittances
INSERT INTO remittances (customer_id, reference_id, amount, currency, sender_name, sender_account, recipient_name, recipient_account, recipient_bank, recipient_country, status, transaction_type, purpose, fees, net_amount, initiated_date, processed_date, completed_date) VALUES
('CUST001', 'RF001A', 5000.00, 'USD', 'John Smith', 'ACC001', 'Alice Johnson', 'ACC101', 'Bank of America', 'United States', 'completed', 'domestic', 'Family support', 25.00, 4975.00, '2024-01-15 10:30:00', '2024-01-15 10:35:00', '2024-01-15 14:20:00'),
('CUST002', 'RF002B', 2500.00, 'USD', 'Sarah Johnson', 'ACC002', 'Bob Smith', 'ACC102', 'Wells Fargo', 'United States', 'processing', 'domestic', 'Business payment', 15.00, 2485.00, '2024-01-16 09:15:00', '2024-01-16 09:20:00', NULL),
('CUST003', 'RF003C', 10000.00, 'USD', 'Michael Brown', 'ACC003', 'Carol Davis', 'ACC103', 'Chase Bank', 'United States', 'completed', 'wire_transfer', 'Investment', 50.00, 9950.00, '2024-01-17 11:45:00', '2024-01-17 11:50:00', '2024-01-17 16:30:00'),
('CUST004', 'RF004D', 1500.00, 'USD', 'Emily Davis', 'ACC004', 'David Wilson', 'ACC104', 'Citibank', 'United States', 'pending', 'domestic', 'Personal transfer', 10.00, 1490.00, '2024-01-18 14:20:00', NULL, NULL),
('CUST005', 'RF005E', 7500.00, 'USD', 'David Wilson', 'ACC005', 'Eva Brown', 'ACC105', 'HSBC', 'United Kingdom', 'completed', 'international', 'Education fees', 75.00, 7425.00, '2024-01-19 08:30:00', '2024-01-19 08:35:00', '2024-01-19 12:15:00'),
('CUST006', 'RF006F', 3000.00, 'USD', 'Lisa Anderson', 'ACC006', 'Frank Miller', 'ACC106', 'Deutsche Bank', 'Germany', 'processing', 'international', 'Business expense', 30.00, 2970.00, '2024-01-20 13:10:00', '2024-01-20 13:15:00', NULL),
('CUST007', 'RF007G', 2000.00, 'USD', 'Robert Taylor', 'ACC007', 'Grace Lee', 'ACC107', 'Bank of China', 'China', 'completed', 'international', 'Family support', 20.00, 1980.00, '2024-01-21 16:45:00', '2024-01-21 16:50:00', '2024-01-22 09:30:00'),
('CUST008', 'RF008H', 12000.00, 'USD', 'Jennifer Martinez', 'ACC008', 'Henry Kim', 'ACC108', 'Shinhan Bank', 'South Korea', 'completed', 'wire_transfer', 'Investment', 60.00, 11940.00, '2024-01-22 10:20:00', '2024-01-22 10:25:00', '2024-01-22 15:45:00'),
('CUST009', 'RF009I', 4500.00, 'USD', 'William Garcia', 'ACC009', 'Ivy Chen', 'ACC109', 'Commonwealth Bank', 'Australia', 'processing', 'international', 'Business payment', 45.00, 4455.00, '2024-01-23 12:30:00', '2024-01-23 12:35:00', NULL),
('CUST010', 'RF010J', 1800.00, 'USD', 'Amanda Rodriguez', 'ACC010', 'Jack Wong', 'ACC110', 'DBS Bank', 'Singapore', 'completed', 'international', 'Personal transfer', 18.00, 1782.00, '2024-01-24 15:15:00', '2024-01-24 15:20:00', '2024-01-25 08:45:00')
ON CONFLICT (reference_id) DO NOTHING;

-- Create a function to update the updated_at timestamp
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ language 'plpgsql';

-- Create triggers to automatically update updated_at
CREATE TRIGGER update_customers_updated_at BEFORE UPDATE ON customers FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();
CREATE TRIGGER update_remittances_updated_at BEFORE UPDATE ON remittances FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

-- Grant permissions
GRANT ALL PRIVILEGES ON DATABASE RMagent TO banking_user;
GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO banking_user;
GRANT ALL PRIVILEGES ON ALL SEQUENCES IN SCHEMA public TO banking_user;

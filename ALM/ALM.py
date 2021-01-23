import numpy as np
import pandas as pd

class ALM:
    opening_year = 2020

    # ------------------------------------------------------------------------------
    # --> Contractual management data

    # subscribed contracts
    insured_number = 1
    insured_premium = 1000
    average_age = 50
    contracts_maturity = 10

    # Contract Charges and Fees
    charges_rate = 0.
    fee_pct_premium = 0.
    fixed_fee = 0.
    fixed_cost_inflation = 0.
    redemption_rates = 0.3

    # Revaluation of contracts
    guaranteed_minimum_rate = 0.
    regu_distrib_tech_res = 0.90
    regu_distrib_fin_prod = 0.85
    contra_distrib_fin_prod = 0.90
    repurchase_rate = 0.
    initial_fp_percentage = 0.
    risk_adjustment = 0
    capital_reserve = 0
    ppe = 0

    # taxes
    tax_rate = 0.

    # bonds
    nominal = 100
    coupon_rate = 0.10
    bonds_initial_mv = 15
    bonds_initial_vnc = 10
    alloc_bonds = 0
    alloc_stocks = 1
    alloc_cash = 0

    # stocks
    stocks_initial_mv = 105
    stocks_initial_vnc = 100

    def __init__(self, *initial_data, **kwargs):
        for dictionary in initial_data:
            for key in dictionary:
                setattr(self, key, dictionary[key])
        for key in kwargs:
            setattr(self, key, kwargs[key])

        # set up years indices
        self.years = np.arange(self.opening_year, self.opening_year + self.contracts_maturity)

    def set_default(self):
        self.opening_year = 2020

        # subscribed contracts
        self.insured_number = 1
        self.insured_premium = 1000
        self.average_age = 50
        self.contracts_maturity = 10

        # Contract Charges and Fees
        self.charges_rate = 0.
        self.fee_pct_premium = 0.
        self.fixed_fee = 0.
        self.fixed_cost_inflation = 0.
        self.redemption_rates = 0.3

        # Revaluation of contracts
        self.guaranteed_minimum_rate = 0.
        self.regu_distrib_tech_res = 0.90
        self.regu_distrib_fin_prod = 0.85
        self.contra_distrib_fin_prod = 0.90
        self.repurchase_rate = 0.
        self.initial_fp_percentage = 0.
        self.risk_adjustment = 0
        self.capital_reserve = 0
        self.ppe = 0

        # taxes
        self.tax_rate = 0.

        # bonds
        self.nominal = 100
        self.coupon_rate = 0.10
        self.bonds_initial_mv = 15
        self.bonds_initial_vnc = 10
        self.alloc_bonds = 0
        self.alloc_stocks = 1
        self.alloc_cash = 0

        # stocks
        self.stocks_initial_mv = 105
        self.stocks_initial_vnc = 100

    def load_parameters_from_file(self,file_name):
        pass

    def load_data_from_file(self, file_name, attr_name):
        try:
            self.__setattr__(attr_name, pd.read_csv(file_name, header=None).values[0,:self.contracts_maturity])
        except Exception as e:
            print(f"problem with the input file {file_name} for {attr_name}: ".e)

    def afficher_data(self, attr_name):
        print(f'{attr_name}={self.forward_rates}')

    def report_discount_rate(self):
        """
         Method: report_discount_rate
       ========
        function : create report for the Discount rate

        Parameters: empty
        ==========

        """

        # Deflator - end of year (calculated)
        self.deflator = np.ones(self.forward_rates.shape)
        for i, el in enumerate(1 + self.forward_rates[1:]):
            self.deflator[i] = self.deflator[i-1] / el

        return pd.DataFrame([self.forward_rates,
                               self.liquidity_premium,
                               self.forward_rates + self.liquidity_premium,
                               self.deflator],
                            columns=list(self.years),
                            index=['forward rate 1Y',
                                   'liquidity premium (semi-calculated)',
                                   'forward rate (calculated)',
                                   'Deflator - end of year (calculated)'])

    def report_neutral_risk(self):
        """
         Method: report_neutral_risk
        ========
        function : Assets and market hypotheses

        Parameters: empty
        ==========

        """

        # compute
        # cash flows
        bonds_cash_flows = np.zeros(self.forward_rates.shape)
        bonds_cash_flows[1:] = self.nominal * self.coupon_rate
        bonds_cash_flows[-1] += self.nominal

        # deflated cash flows
        deflated_bonds_cash_flows = np.zeros(self.forward_rates.shape)
        for i in range(1,self.contracts_maturity):
            deflated_bonds_cash_flows[i] = (bonds_cash_flows[i:] * self.deflator[i:]).sum()

        # neutral risk factor
        self.neutral_risk_factor = np.zeros(self.forward_rates.shape)
        if deflated_bonds_cash_flows[1]:
            self.neutral_risk_factor[1:] = self.bonds_initial_mv / deflated_bonds_cash_flows[1]


        bonds_neutral_risk_cash_flows = bonds_cash_flows * self.neutral_risk_factor[1]

        deflated_neutral_risk_bond = (bonds_neutral_risk_cash_flows[1:] * self.deflator[1:]).sum()

        if (self.bonds_initial_mv == deflated_neutral_risk_bond):
            print("check validated -> VA = MV")
        else:
            raise ValueError('VA different than MV, please check neutral risk calculation')

        return pd.DataFrame([bonds_cash_flows,
                               deflated_bonds_cash_flows,
                               self.neutral_risk_factor,
                               bonds_neutral_risk_cash_flows],
                            columns=list(self.years),
                            index=["bonds cash flows " + str(self.contracts_maturity),
                                   "deflated bonds cash flows_" + str(self.contracts_maturity),
                                   "neutral risk_factor " + str(self.contracts_maturity),
                                   "bonds neutral risk cash flows"])


    def assets_variables_projection(self):
        """
         Method: assets_variables_projection
        ========
        function :

        Parameters:
        ==========

        """
        #       bonds portfolio
        # =============================================================================
        #         Bonds
        # =============================================================================
        depreciation = (self.neutral_risk_factor[1] * self.nominal - self.bonds_initial_vnc) / self.contracts_maturity
        depreciation_bonds_vnc = depreciation*np.ones(self.contracts_maturity)

        received_cp = self.neutral_risk_factor[1] * self.nominal * self.coupon_rate
        received_coupon_per_bond = received_cp*np.ones(self.contracts_maturity)

        one_bond_vnc = self.bonds_initial_vnc + depreciation_bonds_vnc
#        one_bond_vnc = pd.DataFrame([one_bond_vnc], columns=years)
        bonds_stock = 0  # TO BE COMPLETED / FORWARD INFOS

        return

        one_bond_mv = np.zeros(self.contracts_maturity)
        one_bond_mv[1:-1] = ((self.coupon_rate * deflator[2:].sum())
                             + deflator[-2:0:-1]) / deflator[1:-1] * self.nominal * neutral_risk_factor[1]
        one_bond_mv[0]  = self.bonds_initial_mv
        one_bond_mv[-1] = self.nominal * neutral_risk_factor[1]

#        bonds_portfolio["one_bond_mv"] = pd.DataFrame([one_bond_mv], columns=years)
        bonds_quantity_bs = bonds_stock / one_bond_mv
        unrealised_bonds_gains = bonds_quantity_bs * (one_bond_mv - one_bond_vnc)
        bond_quant = ((self.ppe + pm + self.capital_reserve) * self.alloc_bonds) / self.bonds_initial_vnc

        bonds_quantity = np.zeros(self.contracts_maturity)
        bonds_quantity[0] = bond_quant
        bonds_quantity[1:] = -bonds_quantity_bs[1:] + bonds_quantity[:-1]
#        bonds_quantity = pd.DataFrame([bonds_quantity], columns=years)

        bonds_vnc = bonds_quantity * one_bond_vnc
        bonds_vnc[0] = bond_quant * self.bonds_initial_vnc
        bonds_mv = bonds_quantity * one_bond_mv
        bonds_mv[0] = bond_quant * self.bonds_initial_mv



        # =============================================================================
        # Stocks
        # =============================================================================


        # =============================================================================
        # Treasury
        # =============================================================================


        # =============================================================================
        # Financial margines
        # =============================================================================

        # =============================================================================
        # Assets base calculation
        # =============================================================================


        # =============================================================================
        # Total assets booked value
        # =============================================================================

        return

    def total_assets_booked_value(self):
        """
         Method: total_assets_booked_valuue
        ========
        function :

        Parameters:
        ==========

        """

        # =============================================================================
        # Total assets market value
        # =============================================================================

        return

    def total_assets_market_value(self):
        """
         Method: total_assets_market_value
        ========
        function :

        Parameters:
        ==========

        """


        return

        # =============================================================================
        # Variation pmvl reference
        # =============================================================================

    def variation_pmvl_reference(self):
        """
         Method: variation_pmvl_reference
        ========
        function :

        Parameters:
        ==========

        """

        return

    # #############################################################################
    #     Cash Flows Projection (Liabilities)
    # #############################################################################

    def cash_flows_liabilities(self):
        """
         Method: cash_flows_liabilities
        ========
        function : flux cash flows liabilities est un DataFrame qui va mapper tous les dico definis en dessous

              1. Liabilities_inputs : dictionnary
              2. benefits_calculation : dictionnary
              3. Capital__reserve : dictionnary
              4. max_loads : dictionnary
              5. gross_revaluations : dictionnary
              6. revaluations : dictionnary
              7. ppe_management : dictionnary
              8. verif_reval_constraints : dictionnary
              9. provisions : dictionnary

        Parameters:
        ==========

        """


        # =============================================================================
        # Liabilities inputs
        # =============================================================================


        # =============================================================================
        # Benefit calculation
        # =============================================================================



        # =============================================================================
        # Calculation of the capitalisation reserve
        # =============================================================================



        # =============================================================================
        # Calculation of max. loads
        # =============================================================================


        # =============================================================================
        # Technical result
        # =============================================================================

        #        cash_flows_liabilities["technical_result"] =

        # =============================================================================
        # Calculation of gross revaluations
        # =============================================================================



        # =============================================================================
        # Calculation of revaluations
        # =============================================================================


        # =============================================================================
        # PPE management
        # =============================================================================


        # =============================================================================
        # Verification of revaluation constraints
        # =============================================================================


        # =============================================================================
        # Calculation of provisions
        # =============================================================================

        return

        # =============================================================================
        # Calculation BEL
        # =============================================================================

    def calculation_BEL(self):
        """
         Method: Calculation_BEL
        ========
        function :

        Parameters:
        ==========

        """


        return

        # =============================================================================
        # Calcul du local gaap pnl
        # =============================================================================

    def local_gaap_pnl(self):
        """
         Method: local_gaap_pnl
        ========
        function :

        Parameters:
        ==========

        """
        return


        # =============================================================================
        # calculation value in force
        # =============================================================================

    def value_in_force(self):
        """
         Method: value_in_force
        ========
        function :

        Parameters:
        ==========

        """


        return

        # =============================================================================
        # Calculation total value options garantees
        # =============================================================================

    def total_value_options_garantees(self):
        """
        Method: total_value_options_garantees
        ========
        function :

        Parameters:
        ==========

        """

        return

    # #############################################################################
    #  Balance Sheet calibration
    # #############################################################################

    def total_liabilities_vnc(self):
        """
         Method: total_liabilities_vnc
        ========
        function :

        Parameters:
        ==========

        """


        return

    def total_liabilities_vm(self):
        """
        Method: total_liabilities_vm
        ========
        function:

        Parameters:
        ==========

        """

        return


